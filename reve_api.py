import requests
import json
import base64


class ReveAPI:
    def __init__(self, api_key: str, base_url: str = "https://api.reve.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        version: str = "latest",
        save_json: str | None = "reve_output.json",
        save_image: str | None = "reve_image.png"
    ) -> dict | None:
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "version": version
        }

        try:
            response = requests.post(
                f"{self.base_url}/image/create",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()

            result = response.json()

            # JSON yanıtını kaydet
            if save_json:
                with open(save_json, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)

            print(f"Request ID: {result.get('request_id')}")
            print(f"Kullanılan kredi: {result.get('credits_used')}")
            print(f"Kalan kredi: {result.get('credits_remaining')}")

            # Base64 görseli PNG'ye dönüştür
            if result.get("image"):
                try:
                    image_data = base64.b64decode(result["image"])

                    if save_image:
                        with open(save_image, "wb") as img_file:
                            img_file.write(image_data)

                    print(f"Görsel şuraya kaydedildi: {save_image}")
                except Exception as e:
                    print(f"Base64 görseli çözümleme başarısız: {e}")

            if result.get("content_violation"):
                print("Uyarı: İçerik politikası ihlali tespit edildi")
            else:
                print("Görsel başarıyla oluşturuldu")

            return result

        except requests.exceptions.RequestException as e:
            print(f"İstek başarısız oldu: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Yanıt ayrıştırılamadı: {e}")
            return None


if __name__ == "__main__":
    # Kendi API anahtarınızı buraya ekleyin
    reve = ReveAPI(api_key="")

    # Sınıfı test edin
    result = reve.generate_image(
        prompt="A serene mountain with a bear",
        save_json="reve_output.json",
        save_image="reve_image.png"
    )