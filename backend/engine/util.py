import requests, base64, hashlib, os
from os import path

cwd = os.getcwd()


def getMD5(data: str):
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def requestGemini(baseUrl: str, soulname: str, imageData: bytes, language: str):
    return requests.post(
        baseUrl,
        json={
            "system_instruction": {
                "parts": [
                    {"text": f"你必须使用【{language}】回答问题。"},
                    {
                        "text": open(
                            path.join(cwd, f"public/prompts/{soulname}.txt"),
                            "r",
                            encoding="utf8",
                        ).read()
                    },
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": "开始游戏。请评估这张艺术品。",
                        },
                        {
                            "inline_data": {
                                "data": base64.b64encode(imageData).decode("utf-8"),
                                "mime_type": "image/jpeg",
                            },
                        },
                    ],
                },
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "verdict": {
                            "type": "BOOLEAN",
                            "description": "上还是不上",
                        },
                        "rating": {
                            "type": "NUMBER",
                            "description": "1到10的数字",
                        },
                        "explanation": {
                            "type": "STRING",
                            "description": "你的评语/解释",
                        },
                    },
                    "nullable": False,
                    "required": ["verdict", "rating", "explanation"],
                },
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_CIVIC_INTEGRITY",
                    "threshold": "BLOCK_NONE",
                },
            ],
        },
        timeout=30,
    ).json()
