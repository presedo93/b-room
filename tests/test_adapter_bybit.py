import httpx
import respx  # type: ignore

from adapters.exchanges.bybit import ByBitClient


def _make_response(category: str = "linear") -> dict:
    return {
        "retCode": 0,
        "retMsg": "OK",
        "result": {
            "category": category,
            "list": [
                {
                    "symbol": "BTCUSDT",
                    "baseCoin": "BTC",
                    "quoteCoin": "USDT",
                },
                {
                    "symbol": "ETHUSDT",
                    "baseCoin": "ETH",
                    "quoteCoin": "USDT",
                },
            ],
        },
    }


@respx.mock
def test_bybit_adapter_maps_response() -> None:
    route = respx.get("https://api.bybit.com/v5/market/instruments-info").mock(
        return_value=httpx.Response(200, json=_make_response("linear"))
    )

    client = ByBitClient()
    items = client.list_instruments("linear")

    assert route.called
    assert len(items) == 2
    assert items[0].exchange == "bybit"
    assert items[0].name == "BTCUSDT"
    assert items[0].kind == "linear"
    assert items[0].base == "BTC"
    assert items[0].quote == "USDT"
