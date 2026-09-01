# Violence and crime visual-semantics research

Date: 2026-09-01 (Asia/Seoul)

Scope: translate the keyword network from ChatGPT conversation `6a967af3-f290-83e8-bcf8-84c08d948f4f` into observable photo-prompt semantics and candidate-pack data. The source conversation is a vocabulary inventory, not a legal opinion or a pixel contract.

## Outcome

- Added 20 narrow visual-obligation profiles.
- Added 66 candidates in 11 complete six-slot clusters: treatment, subject, action, location, prop, and composition.
- Kept broad genre, mood, color, weapon, blood, injury, punishment, conflict, underworld, fear, and darkness words advisory.
- Added no separate moderation tier, safety-profile slot, or automatic negative policy. Image-model safeguards remain external to this semantic data.
- Kept legal and evidentiary claims separate from pixels. A prompt can declare context; a still image can show supporting relations but cannot adjudicate intent, consent, age, protected status, authority, identity, or culpability by itself.

## Research method

The implementation uses three layers:

1. Official meaning boundary: identify the act, target/status, means, purpose, and context that distinguish neighboring concepts.
2. Observable proposition: retain only relations that can be rendered and falsified in a frame or a deliberately designed split-panel/documentary composition.
3. Prompt/runtime boundary: direct exact terms create profile-owned duties; synonyms, genre words, emotional states, and scene furniture remain optional candidate data.

The recurring visual proposition is:

`actor or source → specific target → action, force, control, or documentation mechanism → localized consequence or trace`

For multi-stage crimes, the proposition becomes:

`same victim or group → linked stages or coordinated units → qualifying means or purpose → destination, exploitation, group-specific, or protected-target consequence`

## Authoritative sources and derived dimensions

### WHO: violence

Source: https://www.who.int/publications/i/item/9241545615

Derived dimensions:

- Actual force and threatened force are separate event phases.
- Violence is directed at self, another person, a group, or community; this work covers interpersonal and group-directed relations, not self-harm.
- Injury, death, psychological harm, maldevelopment, and deprivation are possible results, but not every scene needs all of them.

Limit: the WHO framework is a public-health taxonomy, not a render template or a jurisdiction-specific offense definition.

### UNODC ICCS: behavior-first crime classification

Source: https://www.unodc.org/documents/data-and-analysis/statistics/crime/ICCS/ICCS_English_2016_web.pdf

Derived dimensions:

- The classified unit is the behavior constituting an offense.
- Some crimes need intent, victim status, or a sequence of acts in addition to apparent behavior.
- Intentional homicide, assault/threat, abduction, sexual violence, child status, trafficking, terrorism, and justice-process concepts must not be collapsed into a single crime mood.
- Sexual violence requires an unwanted sexual act, attempt, contact, or communication without valid consent or with consent produced by qualifying coercive means.

Limit: ICCS harmonizes statistics; it does not settle domestic criminal liability or make hidden mental states pixel-verifiable.

### FBI offense definitions: robbery, burglary, arson, violent offenses

Source: https://ucr.fbi.gov/crime-in-the-u.s/2018/crime-in-the-u.s.-2018/topic-pages/offense-definitions

Derived dimensions:

- Robbery is a person-facing taking by force or threat, so the property must change control during the confrontation.
- Burglary is unlawful entry into a structure for an offense, so secured-boundary crossing and an interior objective must remain separate from street theft.
- Arson needs willful or malicious burning or attempted burning, so an already burning background does not establish fire-setting causality.

Limit: U.S. statistical definitions are used only for observable distinction; labels and legal elements vary across jurisdictions.

### UN hostage-taking instrument

Source: https://www.un.org/counterterrorism/en/international-legal-instruments

Derived dimensions:

- A captive alone is not enough: the captor's threat against the hostage must compel a third party.
- The communication path to a government, organization, authority, or other outside recipient is a profile-owned relation.

Limit: a single frame may need radio, phone, broadcast, negotiation perimeter, or split-panel context to make the third party visible.

### UN Convention against Transnational Organized Crime

Source: https://sherloc.unodc.org/cld/en/education/tertiary/organized-crime/module-1/key-issues/definition-in-convention.html

Derived dimensions:

- A structured group persists over time and acts together.
- The group pursues serious crime for financial or other material benefit.
- Visual evidence therefore needs differentiated roles, a shared illegal objective, and a proceeds, route, inventory, or handoff trace.

Limit: clothes, ethnicized stereotypes, tattoos, or a dark meeting room do not prove continuing organization or criminal purpose.

### NIJ and NIST: crime-scene and bloodstain documentation

Sources:

- https://nij.ojp.gov/library/publications/crime-scene-investigation-guide-law-enforcement
- https://www.nist.gov/system/files/documents/2023/01/10/OSAC%202023-N-0002%20Standard%20for%20Scene%20Documentation%20Procedures.OPEN%20COMMENT%20VERSION.pdf
- https://www.nist.gov/document/osac-2022-s-0030-standard-methodology-bloodstain-pattern-analysis-version-20

Derived dimensions:

- Preserve access and original location before collection.
- Link overall, midrange, and close-up records.
- Carry a stable evidence identifier, measurement scale, orientation, and location record across views.
- Document observable stain form, distribution, substrate, and location before causal interpretation.

Limit: red color alone does not establish blood, and a still pattern does not uniquely prove weapon, actor, sequence, or cause.

### Convention against Torture, Article 1

Source: https://www.ohchr.org/Documents/Publications/training5Add2en.pdf

Derived dimensions:

- Intentional severe physical or mental suffering.
- A purpose such as information or confession, punishment, intimidation, coercion, or discrimination.
- Infliction by, at the instigation of, or with consent/acquiescence of an official or someone acting officially.
- A specific detainee under custody or control.

Limit: uniform, detention furniture, pain, restraint, or interrogation alone cannot supply every element; official authority and purpose require explicit authorial context.

### Genocide Convention, Article II

Sources:

- https://www.un.org/en/genocide-prevention/definition
- https://www.un.org/en/genocide-prevention/1948-convention

Derived dimensions:

- Special intent to destroy, in whole or in part, a protected group as such.
- One or more enumerated physical acts.
- Deliberate group targeting rather than random victims.
- A coordinated or repeated campaign is useful supporting evidence but does not replace special intent.

Limit: pixels must never infer real nationality, ethnicity, race, religion, or group membership from appearance. The group and intent must be requester-supplied or explicitly fictional/contextual.

### Rome Statute, Article 8: war crimes

Sources:

- https://legal.un.org/icc/statute/99_corr/2.htm
- https://asp.icc-cpi.int/sites/asp/files/asp_docs/Publications/Compendium/RomeStatute-ENG.pdf

Derived dimensions:

- Armed-conflict nexus.
- Protected person, object, or status supplied by context.
- A prohibited act directed at the same protected target.
- A localized consequence at that target.

Limit: battle damage, uniforms, civilian presence, or suffering in a war zone does not by itself establish a war crime.

### OHCHR: extrajudicial, summary, or arbitrary executions

Source: https://www.ohchr.org/sites/default/files/Documents/Publications/FactSheet11rev.1en.pdf

Derived dimensions:

- A specific captive is already under control.
- An authority or executioner organizes a killing procedure.
- Fixed placement, command, or synchronized action separates execution from impulsive murder or active combat.
- Legal subtype must come from authorial context, not the visual arrangement alone.

Limit: this profile encodes the observable execution event; it does not declare legality, trial fairness, or state responsibility.

### Convention on the Rights of the Child and UNICEF child protection

Sources:

- https://www.unicef.org/child-rights-convention/convention-text
- https://data.unicef.org/topic/child-protection/overview/

Derived dimensions:

- Child-protection violations include violence, exploitation, abuse, neglect, and harmful practices.
- The runtime profile requires requester-declared under-eighteen status plus one named concrete crime.
- A specific offender-to-minor relation and same-event consequence, escape, or protective intervention are required.

Limit: pixels alone do not prove age. Body size, face, clothing, and school context cannot be the sole activation basis.

### Palermo Protocol: trafficking in persons

Source: https://www.unodc.org/documents/treaties/guides/Trafficking_Guide_e.pdf

Derived dimensions:

- Action: recruitment, transportation, transfer, harboring, or receipt.
- Means for adults: force, threat, coercion, abduction, fraud, deception, abuse of power/vulnerability, or controlling payments/benefits.
- Purpose: exploitation, including forced labor, servitude, slavery-like practices, sexual exploitation, or organ removal.
- One victim must remain continuous across the chain.

Limit: smuggling, travel, kidnapping, document retention, or a bad workplace alone does not establish the full trafficking chain.

### UN financing-of-terrorism convention, Article 2

Source: https://www.un.org/law/cod/finterr.htm

Derived dimensions:

- Death or serious bodily injury is directed at civilians or noncombatants.
- The purpose is to intimidate a population or compel a government or international organization.
- A public venue, broadcast, demand, or notification channel can make public reach visible.

Limit: ideology, armed actors, an explosion, public fear, protest, or ordinary combat alone does not establish terrorism or its purpose.

## Twenty promoted visual profiles

| Profile | Minimum visible proposition | Nearest rejected substitutes |
|---|---|---|
| `interpersonal_credible_threat_relation` | adult actor, specific adult target, directed credible threat, target response | generic hostility, weapon portrait |
| `interpersonal_physical_assault_event` | assailant, adult target, contact path, same-point consequence | sport, stage combat, accidental collision |
| `robbery_forced_property_transfer` | offender, property holder, force/threat, victim-to-offender transfer | theft without confrontation, payment |
| `forced_relocation_abduction_event` | abductor, adult captive, control, origin-to-destination movement | arrest, rescue, travel |
| `hostage_third_party_compulsion` | captor, adult hostage, conditional threat, third-party demand | captivity without demand |
| `fictional_intentional_homicide_causality` | declared fictional perpetrator, adult victim, deliberate fatal path, terminal result | accident, combat, aftermath-only |
| `fictional_organized_crime_operation` | continuing group, differentiated roles, illegal objective, benefit trace | gang styling, lawful logistics |
| `deliberate_arson_causality` | fire-setter, property target, ignition path, same-origin fire growth | existing fire, wildfire, accident |
| `burglary_forced_entry_crime_event` | intruder, secured boundary, fresh defeat, interior objective | trespass, locksmith, rescue entry |
| `retaliatory_violence_prior_harm_relation` | prior harm, retaliator-target link, new reprisal, continuity trace | anger or attack without history |
| `forensic_scene_documentation_process` | preservation, linked view sequence, identifier/scale, spatial log | yellow-tape styling, random markers |
| `bloodstain_observation_documentation` | declared stain field, substrate boundary, scale/orientation, uncertainty boundary | paint, texture, unique-cause claim |
| `custodial_torture_purpose_relation` | official custody, adult detainee, intentional severe suffering, qualifying purpose | interrogation or injury alone |
| `genocidal_group_destruction_campaign` | declared protected group, explicit destruction intent, coordinated qualifying acts, group-specific consequence | generic massacre, random casualties |
| `armed_conflict_protected_status_breach` | conflict nexus, declared protected target, prohibited act, localized consequence | ordinary combat, war-zone disaster |
| `controlled_execution_custody_causality` | controlled adult captive, authority, ordered procedure, nonreciprocal consequence | combat, impulsive murder, drill |
| `adult_nonconsensual_sexual_violence_relation` | adult roles, declared unwanted act/attempt, invalid consent/coercion, refusal/control relation | consensual intimacy, medical exam |
| `declared_minor_targeted_crime_relation` | declared minor, adult offender, named concrete crime, same-event trace | caregiving, drill, age inference |
| `adult_human_trafficking_exploitation_chain` | adult victim, trafficking action, coercive/deceptive means, exploitation destination | smuggling, voluntary work, kidnapping-only |
| `terrorism_civilian_coercion_purpose_relation` | civilian target, serious act/threat, public reach, intimidation/compulsion purpose | combat, protest, accident, private crime |

## Candidate-pack coverage

Each semantic cluster owns exactly one candidate in each of six slots:

- `aesthetic_trend`: treatment and evidence priority, never a legal shortcut.
- `subject`: role cardinality and actor/target separation.
- `action`: force, control, documentation, or multi-stage causal mechanism.
- `location`: boundaries, routes, protected context, or fixed landmarks.
- `prop`: ownership, custody, demand, identifier, status, or continuity evidence.
- `composition`: a frame or split-panel layout that preserves the entire relation.

The 11 clusters bind all 20 profiles while letting broad vocabulary remain optional:

1. interpersonal violence
2. coercive capture and property crime
3. fatal, fire-setting, and execution causality
4. organized-crime operation
5. forensic documentation
6. custodial torture
7. mass atrocity
8. adult sexual violence
9. crimes targeting a declared minor
10. adult trafficking in persons
11. terrorism with civilian/public compulsion relation

## Reference-image boundary for render tests

The supplied portrait is used only for visible adult appearance continuity: face shape, facial features, long dark center-parted wavy hair, and calm baseline expression where the selected role allows. It does not supply identity, same-person status, ethnicity, nationality, religion, age proof, criminal role, consent, protected status, health, attractiveness, or personality.

## Test and promotion boundary

- Structural PASS: registry schema, exact routing, negative controls, candidate loading, cluster binding, source evidence, and generated index ownership.
- Prompt PASS: each independent arm receives its selected profile and all required literal evidence fields without candidate-pack override.
- Pixel PASS: every precommitted hard gate must be visible at its assigned scale; partial is failure.
- User judgment: remains separate from technical pixel review.

No source image, generated prompt, or candidate pack is evidence that a real crime occurred.
