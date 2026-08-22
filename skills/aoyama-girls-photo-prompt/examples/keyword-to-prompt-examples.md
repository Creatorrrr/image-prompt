# Keyword-to-Prompt Examples

Use examples to understand transformations, not as reusable content. Preserve a new user's anchors and derive new scene logic.

## Single image

Input:

    mode: single
    keywords: 퇴근, 셀프세탁소, 흰 셔츠, 사원증을 푸는 손, 조용한 안도감, 접힌 책, 50mm, 4:5

Interpretation:

- Theme: See an office worker in a neighborhood laundromat from the conversational distance of a familiar colleague, while public composure begins to loosen into private relief.
- Meaning core: one hand has just lifted the lanyard free and pauses above the folded book when the dryer stops.
- SIR: the lanyard and shirt carry Symbolicity; the folded book and cuff habit carry Individuality; off-axis awareness of a familiar camera carries Relationship.
- Frame: 50mm and 4:5 keep natural proximity, the hand-action, upper body, and enough washer geometry to make the place necessary.

Final Prompt:

    A photorealistic, naturalistic editorial photograph in a modest neighborhood self-service laundromat just after work. An office worker in a slightly creased white shirt sits beside a turning dryer; she has just lifted the identification lanyard over her head, and at the shutter moment one hand pauses above a repeatedly read paperback with a folded corner as the machine stops, while the other still holds a loosened cuff. The camera belongs to a familiar colleague at conversational distance and eye level. She knows it is there but keeps her gaze on the dryer, the last trace of workplace composure easing from her shoulders. Preserve a small eyebrow asymmetry, the cuff-pinching habit, and the worn book edge. Use a vertical 4:5 frame with a natural 50mm perspective, moderate depth of field, and only the washer door, laundry basket, lanyard, and book as meaningful cues. Mixed early-evening window light and ordinary laundromat practical light, restrained contrast, recoverable skin and shirt texture, slight everyday grain. Leave unresolved whether she is waiting to speak or simply enjoying the silence. Real surfaces, no beauty-advertising polish, no text or watermark.

Negative Prompt:

    generic fashion model, glamour pose, seductive eye contact, luxury laundromat, neon decoration, unrelated coffee or flowers, flawless plastic skin, heavy cinematic color grade, extreme bokeh that erases the washers, meaningless body crop, extra people, duplicate objects, malformed hands, logos, watermark

## Parts image

Input:

    mode: parts
    keywords: 비 오는 날 귀가, 현관, 젖은 운동화 끈을 푸는 손, 오래된 친구의 시선, 1:1

Expected transformation:

- Center the hand-shoelace-threshold relation rather than an isolated hand.
- Include just enough wet floor, familiar threshold wear, and the second shoe to communicate return.
- Express the friend's presence through near eye-level placement and accepted proximity.
- Use 1:1 because the sign and interpretive space matter more than a full body.

## Series

Input:

    mode: series
    count: 8
    keywords: 비 오는 회사 옥상, 검은 원피스, 출입카드, 오래된 동료, 떠나기 전의 침묵

Expected transformation:

- Lock subject identity, dress, access card, rooftop geography, wet surfaces, colleague viewpoint, and weather progression.
- Vary narrative roles and distances rather than generating eight hero-pose variants.
- Use the access card first as social role, then as a personal action object, and finally as an unresolved departure cue.

## Revise

Input:

    mode: revise
    problem: 너무 일반적인 패션 화보처럼 보이고 인물과 장소의 관계가 약하다.
    prompt: A stunning woman in a white shirt standing in a beautiful cafe, cinematic lighting, shallow depth of field, elegant pose.

Expected repair:

- Remove generic beauty praise.
- Choose why this particular cafe and person belong together.
- Define the viewer relationship.
- Replace the elegant pose with an incomplete action.
- Add one personal use-mark anchor.
- Preserve only motivated lens and light choices.

