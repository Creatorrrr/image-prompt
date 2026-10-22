# B camera, visibility and contact review before retrieval

Frozen core canonical SHA-256: 7c6e4cdc47fa414d666a9645d050100025333e517a300edd8f929eb9b8fe859f
Frozen baseline text SHA-256: 19677d616b15961215049c06ae735e7d161d4f3b817fea5e52e0ecdae1a7e41f

This memo uses only B's own frozen core, its independently authored direction and preregistered pixel testcase. No candidates, research material or another arm were read. It does not modify the core, slot plan, requester locks or final prompt. The observations below are planned geometric plausibility, not rendered proof.

## Carrying frame

The scanner ring and patient platform must be read as one diagnostic apparatus. Its aperture and the doorway behind it need a common depth relation. The woman stands beside the platform, never coincident with it. Her near palm touches the outside of the ring; the wrist, bent forearm and shoulder must be traceable to the same woman. Her head/gaze and paused posture connect her response to the apparatus rather than to an unexplained offscreen event.

## Main camera conflict

A perfectly frontal view down the scanner bore would show the route clearly but tend to show the back of a person looking through it. A strict side view would show her face but flatten the bore and conceal the doorway relation. The authored three-quarter side view is feasible only as an oblique compromise: the scanner remains a legible open ellipse, the doorway edge and corridor are still visible through it, and her face turns partly toward the observer while her eyes remain directed toward the opening. The head and gaze directions need not be identical, but their difference must remain modest. A far-side profile that removes both eyes from assessment would fail B01 or B05 rather than earn an inferred pass.

A possible later local composition refinement, within the already open camera/framing/pose choices, is to clarify an oblique position near the scanner's room-side flank and state that her near cheek, her bent contacting arm, the aperture and the doorway remain visible together. This is a draft option only. Do not append it to runtime after audit; any actual choice belongs in the composed prompt and a fresh postcomposition review.

## Contact geometry

The contacting palm lies on the scanner's near exterior rim at about shoulder height. The elbow is bent, so the upper arm need not extend through the gantry and the wrist need not fold backward. The contact is a resting touch; her body is supported by her own standing legs beside the platform. There is no requirement to make the scanner support her weight or to depict her pushing a heavy mobile machine. The right arm remains beside the torso. A platform edge that hides the contacting wrist or a rim merged with the fingers makes the full contact gate fail.

## Depth and visibility allocation

The face, contact and scanner aperture are the primary information. The patient platform must have a visible attachment or continuous structure into the gantry, rather than merely align in projection. The doorway frame should provide a distinct boundary behind the ring. Dark corridor contrast may communicate empty depth, but it must not erase the threshold. A low camera would risk the platform masking the arm and route; an elevated camera could dilute the human presence and the spatial obstruction. A moderate oblique human-height view is the current starting option. Lighting must separate the palm from plastic, face from hair, ring from doorway and bed from floor without replacing the central connection with an ornamental light halo.

The baseline frames the woman from head to below the knees. That can support face, torso and hand assessment but may omit feet and the scanner wheels. Standing balance can remain plausible from the body, yet unseen wheel mobility or exact foot placement cannot be claimed. B02 deliberately tests the gantry and attached patient platform; mobility is a separate supplemental observation. If either required object endpoint is cropped, obscured or too small, B02/B03/B04 is partial and fails under the preregistered rules.

## Claim limits and likely failure modes

The visible doorway can be obstructed; a single frame cannot prove it is the only possible exit outside the photographed area. The expression can read as tension; it cannot prove the reference person's actual mental state, illness or consent. The face and short hair can resemble appearance guidance; that is not identity verification. Clinical equipment and cold lighting alone may still produce a neutral examination-room portrait. B06 requires image-grounded unease from the connected person-device-space arrangement; source labels or metadata do not satisfy it.

Likely failures to preserve honestly are: ring used as decorative halo, patient table detached or geometrically merged, doorway lost in shadow, palm hovering at rim, face turned too far away, route visually open despite the written obstruction, and neutral clinical mood. UNOBSERVABLE_NOT_PASS and partial_is_fail apply to every multi-component relation. A local crop cannot replace the whole-image relation.

## Runtime preparation notes

Read latest references/photo-workflow.md and references/image-runtime.md plus the system imagegen skill. The allowed runtime is the built-in image_gen tool with the exact audited prompt and actual local portrait reference attached. The reference has already been directly viewed in this arm; inspect it again if its bytes change or before final execution as needed. Generation remains prohibited until parent installation-complete signal and later instruction. No API fallback, extra image attempt, shared source change or runtime pointer change is authorized by this memo.

The current managed run is mode=prompt_only. The workflow documentation says prompt-only runs reject actual rendering. Before actual native execution, use the supported image-mode replay path with the same independently frozen authored inputs and preserve this run's evidence; do not hand-edit its state. Parent has been informed.
