# Behavioral Acceptance Cases

These cases validate decisions and outputs, not exact headings or wording.

## Case 1: Sparse keywords

Input:

    여름 오후, 방, 선풍기, 읽다 만 책

Pass conditions:

- The four input anchors remain literal.
- The result states any consequential assumptions.
- Three theme candidates differ in relationship or state transition, not only styling.
- The selected image has a visible previous, current, and next action.
- Added room cues fit the information budget.

## Case 2: Technical anchors

Input:

    야근 뒤 버스 정류장, 우산을 접는 손, 35mm, 가로 3:2, 형광등

Pass conditions:

- 35mm, 3:2 horizontal, and fluorescent light remain unchanged.
- The rationale explains what environment the 35mm frame retains.
- The prompt does not replace fluorescent light with fashionable sunset backlight.

## Case 3: Meaning-led detail

Input:

    mode: parts
    keywords: 빵집 마감, 앞치마 매듭을 푸는 손, 오래 쓴 연필, 1:1

Pass conditions:

- The crop centers an action-detail junction, not an isolated body fragment.
- At least one clue communicates work and one communicates individuality.
- The frame widens only enough to make the action and role readable.

## Case 4: Relationship changes composition

Compare:

    A: 친한 친구가 방에 놀러 온 시선
    B: 복도 건너편의 조용한 관찰자 시선

Pass conditions:

- A and B differ in physical distance, awareness, gaze, and framing.
- They are not the same prompt with a relationship label swapped.

## Case 5: Series continuity

Input:

    mode: series
    count: 8
    keywords: 퇴근, 동네 세탁소, 사원증, 접힌 책

Pass conditions:

- A series thesis and continuity lock are present.
- All eight frames have distinct narrative roles and shot deltas.
- Identity, room geography, object state, and time progression remain coherent.
- The sequence includes opening place, chosen self-presentation, relationship, symbolic detail, personal habit, restored distance, and open ending.

## Case 6: Scoped revision

Input:

    mode: revise
    problem: 장소가 장식처럼 보인다.
    prompt: a supplied prompt with explicit clothing, action, lens, and aspect ratio

Pass conditions:

- Explicit clothing, action, lens, and aspect ratio are preserved.
- Only place necessity, related cues, and any directly conflicting composition are changed.
- The response does not rewrite the subject into the skill's preferred archetype.

## Case 7: Prompt and render evidence

Input:

    프롬프트 작성하고 이미지 생성해줘.

Pass conditions:

- Prompt QA occurs before generation.
- A real render is attempted.
- The result reports the final prompt, saved workspace path, and pixel-level observations separately.
- A prompt-only pass is never described as a successful image.

## Case 8: Style-token independence

Pass conditions:

- The generator-ready prompt contains no photographer name.
- The method is expressed through observable theme, distance, action, framing, light, and selection instructions.
- Surface clichés are not substituted for the governing principles.

