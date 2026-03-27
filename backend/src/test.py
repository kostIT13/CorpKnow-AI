from src.services.rag.chroma_client import chroma_client

user_id = "ТВОЙ_USER_ID"  # ← Замени на свой
collection = chroma_client.get_or_create_collection(user_id)

all_docs = collection.get(include=["metadatas", "documents"])

print(f"📊 Всего чанков: {len(all_docs['ids'])}")

from collections import Counter
filenames = Counter(m.get("filename") for m in all_docs.get("metadatas", []) if m and m.get("filename"))

print(f"\n📁 Документы в индексе:")
for filename, count in filenames.most_common():
    print(f"  ✅ {filename}: {count} чанков")

# 🔹 Проверка конкретного файла
if "test2.txt" not in filenames:
    print(f"\n❌ test2.txt НЕ найден в индексе!")
    print("Возможные причины:")
    print("  1. Документ ещё обрабатывается (статус != completed)")
    print("  2. Ошибка при индексации (проверь логи)")
    print("  3. Другой user_id у документа")