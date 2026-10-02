// @exec: {"yield_time_ms": 120000, "max_output_tokens": 1000}
const capture = eval(load("photo_error_capture_source"));
const args = load("photo_native_args");
const composed = load("photo_composed");
const attempt = load("photo_attempt");
const started_at = new Date().toISOString();
store("photo_native_started_at", started_at);
store("photo_native_call_count", 1);
let result;
try {
  result = await tools.image_gen__imagegen(args);
} catch (thrown) {
  const evidence = capture(thrown, {
    tool: "image_gen.imagegen", generation_environment: "codex_native", attempt,
    started_at, ended_at: new Date().toISOString(),
    prompt_en: composed.prompt_en, negative_en: composed.negative_en ?? null,
    runtime_prompt_en: args.prompt
  });
  store("photo_attempt_error_evidence", evidence);
  const quote = value => "'" + value.replaceAll("'", "'\\''") + "'";
  const saved = await tools.exec_command({
    cmd: ".venv/bin/python skills/photo-prompt-image-generator/scripts/image_attempt_evidence.py --write-json " +
      quote(load("photo_error_evidence_path")) + " <<'PHOTO_NATIVE_ERROR_JSON'\n" +
      JSON.stringify(evidence) + "\nPHOTO_NATIVE_ERROR_JSON",
    workdir: load("photo_runtime_workdir"), login: false, max_output_tokens: 1000
  });
  if (saved.exit_code !== 0) throw new Error("Error evidence save failed; do not retry the image call");
  store("photo_attempt_error_file", JSON.parse(saved.output));
  text({attempt, status: evidence.outcome.status,
    request_id: evidence.outcome.request_id, fidelity: evidence.raw_error.fidelity});
}
store("photo_native_ended_at", new Date().toISOString());
if (result !== undefined) {
  store("photo_native_result", result);
  generatedImage(result);
}
