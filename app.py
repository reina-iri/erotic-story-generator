import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.formatters import format_story_output
import os

# ==========================
# Модель
# ==========================
# Укажите путь к модели (локальный или huggingface)
MODEL_NAME = os.environ.get("MODEL_NAME", "TheBloke/MythoMax-L2-13B-GPTQ")

# Опции AutoGPTQ (4-bit)
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)

# ==========================
# Подготовка промпта
# ==========================
SYSTEM_PROMPT_TEMPLATE = """You are an erotic storyteller. 
Write a story in English from the first-person perspective of a passionate married woman. 
Genre: {genre}. 
Mood: {mood}. 
Scene (theme): {theme}. 
Story length: {length}.

Requirements:
- Use present tense
- Add emotional depth, sensory detail, and dirty talk
- Make the character feel real
- Keep the story from a female POV ("I am a married woman who...")

Respond with the full story only.
"""

def generate_prompt(theme, genre, mood, length):
    return SYSTEM_PROMPT_TEMPLATE.format(
        theme=theme, genre=genre, mood=mood, length=length
    )

# ==========================
# Генерация текста
# ==========================
def generate_story(theme, genre, mood, length, tags, prompt1, prompt2, prompt3, num_stories=1):
    stories = []
    
    prompt_text = generate_prompt(theme, genre, mood, length)
    
    generation_params = {
        "max_new_tokens": 512 if length == "long" else 256,
        "do_sample": True,
        "top_p": 0.9,
        "temperature": 1.2
    }
    
    for _ in range(num_stories):
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(**inputs, **generation_params)
        story_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Удаляем возможный повтор system-prompt в начале:
        if story_text.startswith(prompt_text):
            story_text = story_text[len(prompt_text):].strip()
        
        # Форматируем текст (заголовок, абзацы, теги, промпты)
        formatted = format_story_output(story_text, theme, genre, mood, length, tags, [prompt1, prompt2, prompt3])
        stories.append(formatted)

    return "\n\n---\n\n".join(stories)

# ==========================
# Gradio-интерфейс
# ==========================
def gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Erotic Story Generator (MythoMax-L2-13B-GPTQ)\n\nGenerate erotic stories from a married woman's POV.")

        with gr.Row():
            theme = gr.Textbox(label="Тема / Сцена", placeholder="Например: Запретная встреча в роскошном отеле...")

        genre = gr.Dropdown(
            choices=[
                "Fantasy", "Sci-Fi", "BDSM", "Lesbian", "Taboo", "Voyeur", 
                "Incubus/Succubus", "Harem", "Interracial", "Public/Exhibitionism",
                "Cheating/Married Woman", "OnlyFans/Filming", "Sabor Latino",
                "Celebrity", "Anal", "Gang/Group", "Threesome"
            ],
            label="Жанр",
            value="Fantasy"
        )

        mood = gr.Dropdown(
            choices=[
                "Romantic", "Filthy", "Dominant", "Submissive", "Emotional", 
                "Forbidden", "Teasing", "Rough", "Tender", "Playful", 
                "Cruel", "Drunk", "Enchanted", "Sacred", "Humiliated"
            ],
            label="Настроение",
            value="Romantic"
        )

        length = gr.Dropdown(
            choices=["short", "medium", "long"],
            label="Длина текста",
            value="medium"
        )

        tags = gr.Textbox(label="Теги", placeholder="Например: #forbidden #hotel #seduction")

        with gr.Row():
            prompt1 = gr.Textbox(label="Art Prompt 1", placeholder="Prompt для арты №1")
            prompt2 = gr.Textbox(label="Art Prompt 2", placeholder="Prompt для арты №2")
            prompt3 = gr.Textbox(label="Art Prompt 3", placeholder="Prompt для арты №3")

        output_area = gr.Textbox(label="Сгенерированная история", lines=16)

        with gr.Row():
            generate_btn = gr.Button("Generate Story")
            generate_3_btn = gr.Button("Generate 3 Stories")
            copy_btn = gr.Button("Copy All")
            download_btn = gr.DownloadButton("Save as TXT", file_name="erotic_story.txt", file_type="text")

        def on_generate(theme, genre, mood, length, tags, p1, p2, p3):
            return generate_story(theme, genre, mood, length, tags, p1, p2, p3, num_stories=1)

        def on_generate_3(theme, genre, mood, length, tags, p1, p2, p3):
            return generate_story(theme, genre, mood, length, tags, p1, p2, p3, num_stories=3)

        generate_btn.click(on_generate, [theme, genre, mood, length, tags, prompt1, prompt2, prompt3], [output_area])
        generate_3_btn.click(on_generate_3, [theme, genre, mood, length, tags, prompt1, prompt2, prompt3], [output_area])

        copy_btn.click(None, [], [], _js="""
            function() {
                const text = document.querySelector('textarea[aria-label="Сгенерированная история"]').value;
                navigator.clipboard.writeText(text);
                alert('Текст скопирован в буфер обмена!');
            }
        """)

        def download_txt(story_text):
            return story_text
        download_btn.click(download_txt, [output_area], [download_btn])

    return demo

if __name__ == "__main__":
    demo = gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
