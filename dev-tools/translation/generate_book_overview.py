#!/usr/bin/env python3
"""Generate the Spanish book overview from validated compendium names."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "dev-tools/export/data/dnd-tashas-cauldron.tcoe-content.en.json"
OUTPUT = ROOT / "dev-tools/translation/reviewed-content.batch-31.json"
ENTRY_ID = "tcoeUsingThisBoo"
PAGE_ID = "QnrU7PvgLZ7X10mQ"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    source = load(SOURCE)["entries"][ENTRY_ID]["pages"][PAGE_ID]["text"]
    packs = {
        path.stem.removeprefix("dnd-tashas-cauldron."): load(path)
        for path in (ROOT / "compendium").glob("dnd-tashas-cauldron.*.json")
    }
    label_overrides = {
        "Chapter 1": "Capítulo 1", "Chapter 2": "Capítulo 2", "Chapter 4": "Capítulo 4",
        "Chapter 1: Character Options": "Capítulo 1: Opciones de personaje",
        "Chapter 2: Group Patrons": "Capítulo 2: Patrones de grupo",
        "Chapter 3: Magical Miscellany": "Capítulo 3: Miscelánea mágica",
        "Chapter 4: Dungeon Master's Tools": "Capítulo 4: Herramientas del Dungeon Master",
        "Customizing Your Origin": "Personalizar tu origen", "Changing a Skill": "Cambiar una habilidad",
        "Changing Your Subclass": "Cambiar tu subclase", "Optional Class Features": "Rasgos de clase opcionales",
        "Optional Class Feature": "Rasgo de clase opcional", "Class Features": "Rasgos de clase",
        "Artificer": "Artífice", "Armorer": "Armero", "Battle Smith": "Herrero de batalla",
        "Barbarian": "Bárbaro", "Path of the Beast": "Senda de la Bestia",
        "Path of Wild Magic": "Senda de la Magia Salvaje", "Bard": "Bardo",
        "College of Creation": "Colegio de la Creación", "College of Eloquence": "Colegio de la Elocuencia",
        "Cleric": "Clérigo", "Order Domain": "Dominio del Orden", "Peace Domain": "Dominio de la Paz",
        "Twilight Domain": "Dominio del Crepúsculo", "Druid": "Druida",
        "Circle of Spores": "Círculo de las Esporas", "Circle of Stars": "Círculo de las Estrellas",
        "Circle of Wildfire": "Círculo del Fuego Salvaje", "Fighter": "Guerrero",
        "Psi Warrior": "Guerrero Psiónico", "Rune Knight": "Caballero Rúnico", "Monk": "Monje",
        "Way of Mercy": "Camino de la Misericordia", "Way of the Astral Self": "Camino del Yo Astral",
        "Paladin": "Paladín", "Oath of Glory": "Juramento de Gloria",
        "Oath of the Watchers": "Juramento de los Vigilantes", "Ranger": "Explorador",
        "Fey Wanderer": "Errante Feérico", "Swarmkeeper": "Guardaenjambres",
        "Beast Master Companions": "Compañeros del Señor de las Bestias", "Rogue": "Pícaro",
        "Phantom": "Fantasma", "Soulknife": "Rebanaalmas", "Sorcerer": "Hechicero",
        "Aberrant Mind": "Mente Aberrante", "Clockwork Soul": "Alma Mecánica", "Warlock": "Brujo",
        "Eldritch Invocation Options": "Opciones de invocación sobrenatural", "The Fathomless": "El Insondable",
        "The Genie": "El Genio", "Wizard": "Mago", "Bladesinging": "Canto de la Hoja",
        "Order of Scribes": "Orden de los Escribas", "How Patrons Work": "Cómo funcionan los patrones",
        "Example Patrons": "Ejemplos de patrones", "Being Your Own Patron": "Ser tu propio patrón",
        "Spells": "Conjuros", "Tasha's Complete Spell List": "Lista completa de conjuros de Tasha",
        "Personalizing Spells": "Personalización de conjuros", "Magic Items": "Objetos mágicos",
        "Magic Tattoos": "Tatuajes mágicos", "Session Zero": "Sesión cero",
        "Character and Party Creation": "Creación de personajes y del grupo", "Social Contract": "Contrato social",
        "Game Customization": "Personalización del juego", "Sidekicks": "Acompañantes",
        "Parleying with Monsters": "Negociar con monstruos", "Environmental Hazards": "Peligros ambientales",
        "Puzzles": "Rompecabezas", "Credits & License": "Créditos y licencia",
        "items": "objetos", "magic-infused tattoos": "tatuajes imbuidos de magia",
    }

    pattern = re.compile(
        r"@UUID\[Compendium\.dnd-tashas-cauldron\.([^.]+)\.(?:JournalEntry|Item)\.([^.\]]+)"
        r"(?:\.JournalEntryPage\.([^\]]+))?\]\{([^}]*)\}"
    )

    def translate_label(match: re.Match[str]) -> str:
        pack, entry_id, page_id, original = match.groups()
        translated = label_overrides.get(original)
        row = packs.get(pack, {}).get("entries", {}).get(entry_id, {})
        if not translated and page_id:
            translated = row.get("pages", {}).get(page_id, {}).get("name")
        if not translated:
            translated = row.get("name")
        if not translated:
            raise KeyError(f"Missing translated label: {pack}/{entry_id}/{page_id} ({original})")
        prefix = match.group(0).split("{", 1)[0]
        return f"{prefix}{{{translated}}}"

    text, linked = pattern.subn(translate_label, source)
    replacements = {
        "<p><em>Tasha’s Cauldron of Everything</em> offers a host of new options for Dungeons &amp; Dragons, and our journey through those options is accompanied by the notes of the wizard Tasha. Creator of the spell @UUID[Compendium.dnd5e.spells.Item.BQk5Row4NymMnUQl]{Tasha's Hideous Laughter}, Tasha’s life is one of the most storied in the D&amp;D multiverse. Raised by Baba Yaga, the Mother of Witches herself, Tasha adventured across the world of Greyhawk and became the friend and sometimes enemy of other famous adventurers, like Mordenkainen. In time, she ruled as the Witch Queen and later changed her name to Iggwilv—a figure of legend who is whispered about, feared, and admired.</p>": "<p><em>El Caldero de Tasha para Todo</em> ofrece multitud de opciones nuevas para Dungeons &amp; Dragons, y las notas de la maga Tasha acompañan nuestro recorrido por ellas. Creadora del conjuro @UUID[Compendium.dnd5e.spells.Item.BQk5Row4NymMnUQl]{Risa horrible de Tasha}, su vida es una de las más legendarias del multiverso de D&amp;D. Criada por la mismísima Baba Yaga, la Madre de las Brujas, Tasha vivió aventuras por el mundo de Falcongrís y fue amiga y, en ocasiones, enemiga de otros aventureros famosos, como Mordenkainen. Con el tiempo gobernó como Reina Bruja y más tarde adoptó el nombre de Iggwilv, una figura legendaria de la que se habla en susurros y que inspira miedo y admiración.</p>",
        "<p>Written for players and Dungeon Masters alike, this book offers options to enhance characters and campaigns in any D&amp;D world, whether you’re adventuring in Greyhawk, another official D&amp;D setting, or a world of your own creation.</p>": "<p>Escrito tanto para jugadores como para Dungeon Masters, este libro ofrece opciones para enriquecer personajes y campañas en cualquier mundo de D&amp;D, ya vivas aventuras en Falcongrís, en otro escenario oficial o en un mundo de tu propia creación.</p>",
        "<h1>What You’ll Find Within</h1>": "<h1>Qué encontrarás en el interior</h1>",
        " brims with new features and subclasses for the classes in the Player’s Handbook, and it presents the artificer class, a master of magical invention. The chapter also offers feats for groups that use them.": " rebosa de nuevos rasgos y subclases para las clases del Manual del Jugador, y presenta la clase artífice, maestra de la invención mágica. El capítulo también ofrece dotes para los grupos que las utilicen.",
        " contains patrons who can become one of the driving forces behind your group’s adventures.": " contiene patrones que pueden convertirse en una de las fuerzas motrices de las aventuras del grupo.",
        "<p><strong>Chapter 3</strong> sparkles with new magical options, including ": "<p><strong>El capítulo 3</strong> resplandece con nuevas opciones mágicas, entre ellas ",
        ", magical spellbooks, artifacts, and ": ", grimorios mágicos, artefactos y ",
        "—available for both player characters and monsters to use.</p>": ", disponibles tanto para personajes jugadores como para monstruos.</p>",
        " holds various rules that a DM may incorporate into a campaign, including rules on sidekicks who level up with the player characters and on supernatural environments. The chapter ends with a collection of puzzles ready to be deployed in any adventure that the DM would like to spice up with some puzzling.": " contiene diversas reglas que un DM puede incorporar a una campaña, incluidas reglas para acompañantes que suben de nivel junto a los personajes jugadores y para entornos sobrenaturales. El capítulo termina con una colección de rompecabezas preparados para incluirse en cualquier aventura que el DM quiera sazonar con algún enigma.",
        "<h1>Table of Contents</h1>": "<h1>Índice</h1>",
        "<h1>It’s All Optional</h1>": "<h1>Todo es opcional</h1>",
        "<p>Everything in this book is optional. Each group, guided by the DM, decides which of these options, if any, to incorporate into a campaign. You can use some, all, or none of them. We encourage you to choose the ones that fit best with your campaign’s story and with your group’s style of play.</p>": "<p>Todo el contenido de este libro es opcional. Cada grupo, guiado por el DM, decide cuáles de estas opciones quiere incorporar a la campaña, si es que desea alguna. Puedes usar unas pocas, todas o ninguna. Te animamos a elegir las que mejor encajen con la historia de tu campaña y el estilo de juego del grupo.</p>",
        "<p>Whatever options you choose to use, this book relies on the rules in the Player’s Handbook, Monster Manual, and Dungeon Master’s Guide, and it can be paired with the options in Xanathar’s Guide to Everything and other D&amp;D books.</p>": "<p>Elijas las opciones que elijas, este libro se apoya en las reglas del Manual del Jugador, el Manual de Monstruos y la Guía del Dungeon Master, y puede combinarse con las opciones de la Guía del Xanathar para Todo y otros libros de D&amp;D.</p>",
        "<h3>Unearthed Arcana</h3>": "<h3>Unearthed Arcana</h3>",
        "<p>Much of the material in this book originally appeared in Unearthed Arcana, a series of online articles we publish to explore rules that might officially become part of the game. Some Unearthed Arcana offerings don’t end up resonating with fans and are set aside. The Unearthed Arcana material that inspired the options in the following chapters was well received and, thanks to feedback from thousands of D&amp;D fans, has been refined into the official forms presented here.</p>": "<p>Gran parte del material de este libro apareció originalmente en Unearthed Arcana, una serie de artículos en línea que publicamos para explorar reglas que podrían incorporarse oficialmente al juego. Algunas propuestas no terminan de convencer a los aficionados y se descartan. El material de Unearthed Arcana que inspiró las opciones de los capítulos siguientes fue bien recibido y, gracias a los comentarios de miles de aficionados a D&amp;D, se ha refinado hasta adoptar las versiones oficiales aquí presentadas.</p>",
    }
    for original, translated in replacements.items():
        if original not in text:
            raise ValueError(f"Expected overview fragment not found: {original[:80]}")
        text = text.replace(original, translated)

    payload = {"entries": {ENTRY_ID: {"pages": {PAGE_ID: {"text": text}}}}}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.name} with {linked} synchronized Tasha compendium labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
