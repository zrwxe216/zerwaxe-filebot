import os

def remove_character(content, char_to_remove):
    """Supprime un caractère spécifique dans une chaîne de texte."""
    return content.replace(char_to_remove, "")

def divide_file_content(content, num_parts):
    """Divise le contenu d'un fichier en plusieurs parties."""
    lines = content.splitlines(keepends=True)
    total_lines = len(lines)

    if num_parts <= 0 or num_parts > total_lines:
        return "Nombre de parties invalide."

    lines_per_part = total_lines // num_parts
    extra_lines = total_lines % num_parts

    parts = []
    start = 0
    for i in range(num_parts):
        end = start + lines_per_part + (1 if i < extra_lines else 0)
        parts.append(''.join(lines[start:end]))
        start = end

    return parts
