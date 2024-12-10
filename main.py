import re

def parse_chords_and_lyrics_with_rests(input_text):
    """
    Converts input song text with chords (including rests or pauses) into ChordPro format.
    Assumes chords are written above lyrics in the input.
    """
    lines = input_text.split("\n")
    output_lines = []
    clean_lyrics_history = set()
    
    # Enhanced regex to include '.' or '-' following chords
    chord_regex = r'\(?[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?[\.-]*\)?'
    
    for i in range(len(lines) - 1):
        chords_line = lines[i]
        lyrics_line = lines[i + 1].strip()
        
        # Check if the chords line consists mostly of chords with rests or pauses
        if all(re.match(chord_regex, chord) for chord in chords_line.split()):
            clean_lyrics_history.add(lyrics_line)
            # Map chords with rests to lyrics
            # print("chords_line ", chords_line)
            # print("lyrics_line ", lyrics_line)
            matches = list(re.finditer(chord_regex, chords_line))
            formatted_line = ""
            last_pos = 0
            
            for match in matches:
                chord = match.group(0)
                pos = match.start()
                space_to_fill = pos - last_pos + 1 if pos > 1 else pos - last_pos
                formatted_line += lyrics_line[:space_to_fill] + f"[{chord.strip()}]"
                lyrics_line = lyrics_line[space_to_fill:]
                last_pos = match.end()
            
            formatted_line += lyrics_line
            # print("Formatted line", formatted_line, end="\n \n")
            output_lines.append(formatted_line)
            # Skip next line since we're parsing 2 at a time
            i += 1
        elif chords_line not in clean_lyrics_history:
            output_lines.append(chords_line)
    
    return "\n".join(output_lines)

def convert_to_chordpro(input_file, output_file):
    """
    Reads input song file, converts it to ChordPro format, and writes to output file.
    """
    with open(input_file, 'r', encoding="utf-8") as file:
        input_text = file.read()
    
    chordpro_text = parse_chords_and_lyrics_with_rests(input_text)
    
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(chordpro_text)
    
    print(f"ChordPro formatted file saved to {output_file}")

if __name__ == "__main__":
    # Example Usage
    input_text = """ 
    G       C       D
    Amazing Grace, how sweet the sound
    Em      G       C
    That saved a wretch like me
    """

    file_name = "Test.txt"
    output_name = "output.txt"
    
    # print(parse_chords_and_lyrics(input_text))
    convert_to_chordpro(file_name, output_name)