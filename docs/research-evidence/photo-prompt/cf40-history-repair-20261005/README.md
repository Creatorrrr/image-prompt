# Historical manifest repair

The incoming cf40 commit replaced the V10–V12 manifest observations while retaining their original pack files and the V13–V17 successor chain. The unchanged validator rejects V13 because its predecessor hash no longer matches. The replacement manifests also disagree with their retained pack IDs and SHA256 values.

This repair restores the three historical manifests from the immediate parent 977a and preserves all incoming manifest bytes under `incoming-observations/`. Those copies record incoming observations, not newly validated baselines. `PROVENANCE.json` pins both sources and hashes.

The incoming authoring guidance and production DATA are untouched by this repair. A limited execution of the exact unchanged lineage-validation function reaches the generation step after the repair; it is not a full current-source validator pass. Current DATA and authoring changes still require separately qualified successor evidence.
