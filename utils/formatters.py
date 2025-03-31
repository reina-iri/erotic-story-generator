def format_story_output(story_text, theme, genre, mood, length, tags, prompts):
    """
    Тут можно дорабатывать форматирование (заголовок, переносы строк, теги и т.д.)
    """
    title = f"--- EROTIC STORY ---\nGenre: {genre} | Mood: {mood} | Length: {length}\nTheme: {theme}"
    
    tags_line = ""
    if tags.strip():
        tags_line = f"\nTags: {tags}"
    
    prompts_line = ""
    for i, p in enumerate(prompts, 1):
        if p.strip():
            prompts_line += f"\nArt Prompt {i}: {p}"
    
    paragraphs = [p.strip() for p in story_text.split("\n") if p.strip()]
    formatted_body = "\n\n".join(paragraphs)
    
    formatted_story = f"{title}{tags_line}{prompts_line}\n\n{formatted_body}"
    return formatted_story
