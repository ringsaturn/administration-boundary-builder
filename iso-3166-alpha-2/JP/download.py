import requests


if __name__ == "__main__":
    LANDSLIDES_TPL = "https://www.jma.go.jp/bosai/common/const/geojson/landslides_{idx}.json"
    for idx in range(0, 10):
        url = LANDSLIDES_TPL.format(idx=idx)
        base_name = f"jp_landslides_{idx}.json"
        with open(base_name, "wb") as f:
            f.write(requests.get(url).content)
