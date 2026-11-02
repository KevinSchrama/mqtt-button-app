import paho.mqtt.client as mqtt
from typing import Optional, Callable
from models import ButtonConfig
import threading
import time


class MQTTClientWrapper:
    def __init__(self):
        self._client = None
        self._connected = False
        self._publish_complete = False
        self._publish_success = False
        self._error_message = ""

    def publish(
        self,
        server: str,
        port: int,
        topic: str,
        message: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        qos: int = 0,
        retain: bool = False,
        timeout: int = 10,
    ) -> tuple[bool, Optional[str]]:
        """
        Simple synchronous connect, publish, and disconnect.
        Returns (success, error_message).
        """
        client = mqtt.Client()
        
        if username and password:
            client.username_pw_set(username, password)

        try:
            client.connect(server, port, timeout)
            result = client.publish(topic, message, qos=qos, retain=retain)
            result.wait_for_publish(timeout=timeout)
            client.disconnect()
            return True, None
        except Exception as e:
            error_msg = str(e)
            try:
                client.disconnect()
            except Exception:
                pass
            return False, error_msg

    def publish_message(
        self,
        config: ButtonConfig,
        timeout: int = 10,
        callback: Optional[Callable[[bool, str], None]] = None,
    ) -> bool:
        """
        Async publish with callback. Uses threading to avoid blocking UI.
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self._connected = True
            else:
                self._connected = False
                self._error_message = f"Connection failed with code {rc}"

        def on_publish(client, userdata, mid):
            self._publish_complete = True
            self._publish_success = True

        def on_disconnect(client, userdata, rc):
            self._connected = False

        def run_publish():
            self._client = mqtt.Client()
            self._client.on_connect = on_connect
            self._client.on_publish = on_publish
            self._client.on_disconnect = on_disconnect

            if config.username and config.password:
                self._client.username_pw_set(config.username, config.password)

            try:
                self._client.connect(config.server, config.port, timeout)
                self._client.loop_start()

                start_time = time.time()
                while not self._connected and (time.time() - start_time) < timeout:
                    time.sleep(0.1)

                if not self._connected:
                    self._client.loop_stop()
                    self._client.disconnect()
                    if callback:
                        callback(False, self._error_message or "Connection timeout")
                    return

                result = self._client.publish(
                    config.topic,
                    config.message,
                    qos=config.qos,
                    retain=config.retain,
                )

                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    start_time = time.time()
                    while not self._publish_complete and (time.time() - start_time) < timeout:
                        time.sleep(0.1)

                    if self._publish_complete:
                        if callback:
                            callback(True, "Message published successfully")
                    else:
                        if callback:
                            callback(False, "Publish timeout")
                else:
                    if callback:
                        callback(False, f"Publish failed with code {result.rc}")

            except Exception as e:
                if callback:
                    callback(False, str(e))
            finally:
                self._client.loop_stop()
                self._client.disconnect()
                self._client = None

        thread = threading.Thread(target=run_publish, daemon=True)
        thread.start()
        return True
