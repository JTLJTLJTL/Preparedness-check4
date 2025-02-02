from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ✅ Restore QUESTIONS and RECOMMENDATIONS
QUESTIONS = {
    "general": [
        {"question": "Hast du Zugang zu einem Auto oder einem anderen zuverlässigen Fahrzeug?", "options": ["Ja", "Nein"]},
        {"question": "Hast du in den letzten 5 Jahren einen Erste-Hilfe-Kurs gemacht?", "options": ["Ja", "Nein"]},
        {"question": "Besitzt du dein eigenes Haus oder deine eigene Wohnung?", "options": ["Ja", "Nein"]},
        {"question": "Hast du enge Freunde oder zuverlässige Nachbarn in einem Umkreis von 500m?", "options": ["Ja", "Nein"]},
        {"question": "Gibt es öffentliche Notfallstrukturen (Krankenhaus, Schule, öffentliche Gebäude) in einem Umkreis von 3 km?", "options": ["Ja", "Nein"]}
    ],
    "survival": [
        {"question": "Hast du Vorräte für mindestens 3 Tage (nicht verderbliche Lebensmittel)?", "options": ["Ja", "Nein"]},
        {"question": "Hast du mindestens 3 Liter Trinkwasser pro Person pro Tag?", "options": ["Ja", "Nein"]},
        {"question": "Besitzt du ein voll ausgestattetes Erste-Hilfe-Set?", "options": ["Ja", "Nein"]},
        {"question": "Hast du grundlegende Überlebensausrüstung (Taschenlampe, Heizung, Batterien, Powerbank)?", "options": ["Ja", "Nein"]}
    ],
    "mental": [
        {"question": "Denkst du aktiv über Krisenvorsorge nach und bereitest dich darauf vor?", "options": ["Ja", "Nein"]},
        {"question": "Bist du stark unter Druck?", "options": ["Ja", "Nein"]},
        {"question": "Weißt du, wen du im Notfall als Erstes kontaktieren würdest?", "options": ["Ja", "Nein"]}
    ]
}

RECOMMENDATIONS = {
    "general": [
        "🚗 Besorge dir eine alternative Transportmöglichkeit (Fahrrad, Mitfahrgelegenheit, öffentlicher Nahverkehr).",
        "🩹 Ein Erste-Hilfe-Kurs könnte im Notfall Leben retten – melde dich an!",
        "🏠 Falls du nicht in deiner eigenen Wohnung lebst, plane einen Notfallplan für alternative Unterkünfte.",
        "🤝 Baue dein soziales Netzwerk aus – weißt du, wer dir in einer Krise helfen kann?",
        "🏥 Finde heraus, wo sich in deiner Umgebung Notunterkünfte oder sichere Orte befinden."
    ],
    "survival": [
        "🥫 Lege einen Vorrat an nicht verderblichen Lebensmitteln für mindestens 3 Tage an.",
        "💧 Stelle sicher, dass du mindestens 3 Liter Trinkwasser pro Person und Tag hast.",
        "🩹 Besorge dir ein gut ausgestattetes Erste-Hilfe-Set für dein Zuhause.",
        "🔦 Halte eine Taschenlampe, Ersatzbatterien und eine Notheizung bereit."
    ],
    "mental": [
        "📖 Beschäftige dich aktiv mit Krisenvorsorge – welche Risiken gibt es in deiner Region?",
        "🧘‍♂️ Arbeite an deiner Stressbewältigung – z. B. durch Sport oder Meditation.",
        "📞 Speichere wichtige Notfallkontakte in deinem Telefon oder erstelle eine physische Notfallkarte."
    ]
}

@app.route("/")
def index():
    return render_template("index.html", questions=QUESTIONS)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    answers = data.get("answers", {})

    # Debugging: Print raw received answers
    print("\n🔹 RAW DATA RECEIVED FROM JAVASCRIPT:")
    print(answers)

    total_questions = sum(len(QUESTIONS[cat]) for cat in QUESTIONS)
    yes_count = 0
    no_count = 0

    # Debugging: Check each answer received
    for category, user_answers in answers.items():
        for ans in user_answers:
            ans = ans.strip().lower()
            print(f"Processing answer: '{ans}'")  # Debugging output
            if ans == "ja":
                yes_count += 1
            elif ans == "nein":
                no_count += 1

    print(f"✅ Corrected Yes Count: {yes_count}")
    print(f"✅ Corrected No Count: {no_count}")

    # Fix percentage calculation
    percentage = round((yes_count / total_questions) * 100) if total_questions > 0 else 0
    print(f"📊 FINAL PREPAREDNESS SCORE: {percentage}%")

    # Generate recommendations only for "Nein" answers
    checklist = []
    for category, user_answers in answers.items():
        for idx, answer in enumerate(user_answers):
            if answer.strip().lower() == "nein":
                checklist.append(RECOMMENDATIONS[category][idx])

    print(f"📝 Generated Recommendations: {checklist}")

    if not checklist:
        checklist.append("🎯 Du bist bestens vorbereitet! Schau auf [www.ernstfallbox.de](https://www.ernstfallbox.de) für weitere Inspiration!")

    return jsonify({"percentage": percentage, "evaluation": f"✅ Du hast {percentage}% erreicht!", "checklist": checklist})

if __name__ == "__main__":
    app.run(debug=True)
