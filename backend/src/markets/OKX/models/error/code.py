from typing import Optional

class ErrorCodeTranslator:
    def __init__(self):
        self.error_codes = {
            60004: "Invalid timestamp",
            60005: "Invalid apiKey",
            60006: "Timestamp request expired",
            60007: "Invalid sign",
            60008: "The current WebSocket endpoint does not support subscribing to {0} channels. Please check the WebSocket URL.",
            60009: "Login failure",
            60011: "Please log in",
            60012: "Invalid request",
            60013: "Invalid args",
            60014: "Requests too frequent",
            60018: "Wrong URL or {0} doesn't exist. Please use the correct URL, channel and parameters referring to API document.",
            60019: "Invalid op: {op}",
            60020: "APIKey subscription amount exceeds the limit {0}.",
            60021: "This operation does not support multiple accounts login.",
            60022: "Bulk login partially succeeded",
            60023: "Bulk login requests too frequent",
            60024: "Wrong passphrase",
            60025: "token subscription amount exceeds the limit {0}",
            60026: "Batch login by APIKey and token simultaneously is not supported.",
            60027: "Parameter {0} can not be empty.",
            60028: "The current operation is not supported by this URL. Please use the correct WebSocket URL for the operation.",
            60029: "Only users who are VIP5 and above in trading fee tier are allowed to subscribe to this channel.",
            60030: "Only users who are VIP4 and above in trading fee tier are allowed to subscribe to books50-l2-tbt channel.",
            60031: "The WebSocket endpoint does not allow multiple or repeated logins.",
            60032: "API key doesn't exist",
            63999: "Login failed due to internal error. Please try again later.",
            64000: "Subscription parameter uly is unavailable anymore, please replace uly with instFamily. More details can refer to: https://www.okx.com/help-center/changes-to-v5-api-websocket-subscription-parameter-and-url",
            64001: "This channel has been migrated to the '/business' URL. Please subscribe using the new URL. More details can refer to: https://www.okx.com/help-center/changes-to-v5-api-websocket-subscription-parameter-and-url",
            64002: "This channel is not supported by \"/business\" URL. Please use \"/private\" URL(for private channels), or \"/public\" URL(for public channels). More details can refer to: https://www.okx.com/help-center/changes-to-v5-api-websocket-subscription-parameter-and-url",
            64003: "Your trading fee tier doesn't meet the requirement to access this channel.",
            4001: "Close Frame",
            4002: "Request message exceeds the maximum frame length",
            4003: "Login Failed",
            4004: "Invalid Request",
            4005: "APIKey subscription amount exceeds the limit 100",
            4006: "No data received in 30s",
            4007: "Buffer is full, cannot write data",
            4008: "Abnormal disconnection",
            4009: "API key has been updated or deleted. Please reconnect.",
            4010: "The number of subscribed channels exceeds the maximum limit.",
            4011: "The number of subscription channels for this connection exceeds the limit."
        }

    def translate(self, code: int) -> Optional[str]:
        return self.error_codes.get(code)

# Example usage:

translator = ErrorCodeTranslator()

code_4003 = translator.translate(4003)
print(code_4003)  # Output: Login Failed

code_4010 = translator.translate(4010)
print(code_4010)  # Output: The number of subscribed channels exceeds the maximum limit.

code_99999 = translator.translate(60012)
print(code_99999)  # Output: None (Unknown or not found code)
