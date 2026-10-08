async function makeArm2NativeTools({tools, python, workdir, base, composed}) {
  const quote = s => "'" + String(s).replaceAll("'", "'\\''") + "'";
  async function completedCommand(args) {
    let result = await tools.exec_command({...args, workdir: args.workdir || workdir});
    let output = result.output || "";
    while (result.session_id) {
      result = await tools.write_stdin({session_id: result.session_id, chars: "", yield_time_ms: 1000, max_output_tokens: args.max_output_tokens || 2000});
      output += result.output || "";
    }
    return {...result, output};
  }
  const capture = eval(load("arm2_error_capture_source"));
  const adapted = {
    exec_command: completedCommand,
    image_gen__imagegen: async args => {
      const started_at = new Date().toISOString();
      store("arm2_actual_image_call_count", 1);
      store("arm2_exact_native_payload", args);
      let result;
      try {
        result = await tools.image_gen__imagegen(args);
      } catch (thrown) {
        const evidence = capture(thrown, {
          tool: "image_gen", generation_environment: "native_imagegen", attempt: 1,
          started_at, ended_at: new Date().toISOString(),
          prompt_en: composed.prompt_en, negative_en: composed.negative_en ?? null,
          runtime_prompt_en: args.prompt
        });
        store("arm2_native_error_evidence", evidence);
        const saved = await completedCommand({
          cmd: quote(python) + " " + quote(workdir + "/skills/photo-prompt-image-generator/scripts/image_attempt_evidence.py") +
            " --write-json " + quote(base + "/actual-native-error.json") + " <<'ARM2_NATIVE_ERROR_JSON'\n" +
            JSON.stringify(evidence) + "\nARM2_NATIVE_ERROR_JSON",
          max_output_tokens: 2000, login: false
        });
        if (saved.exit_code !== 0) throw new Error("Actual raw native error could not be saved; do not retry.");
        throw thrown;
      }
      store("arm2_raw_native_result", result);
      return result;
    }
  };
  async function observe(result) {
    const referencePath = "/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg";
    const paths = [];
    function collect(value) {
      if (typeof value === "string") {
        if (value.startsWith("data:")) return;
        if (/^\/.*\.(?:png|jpe?g|webp)$/i.test(value) && value !== referencePath) paths.push(value);
        const expression = /(?:^|\s)(\/(?:Users|mnt|tmp|home)\/[^\n\"<>]*?\.(?:png|jpe?g|webp))(?=\s|$|[\"<>])/gi;
        for (const match of value.matchAll(expression)) if (match[1] !== referencePath) paths.push(match[1]);
      } else if (Array.isArray(value)) {
        for (const item of value) collect(item);
      } else if (value && typeof value === "object") {
        for (const [key, item] of Object.entries(value)) if (!["data", "base64", "b64_json"].includes(key)) collect(item);
      }
    }
    collect(result);
    const distinct = [...new Set(paths)];
    store("arm2_returned_local_path_candidates", distinct);
    if (!distinct.length) return {outcome: "preview_only"};
    const copy = await completedCommand({
      cmd: quote(python) + " - " + quote(distinct[0]) + " " + quote(base) + " <<'ARM2_COPY_PY'\n" +
        "from pathlib import Path\nimport sys,shutil,json,hashlib\n" +
        "src=Path(sys.argv[1]); base=Path(sys.argv[2])\n" +
        "if not src.is_file(): raise SystemExit('tool_returned_path_is_not_a_concrete_file')\n" +
        "dst=base/('initial-native'+src.suffix.lower())\n" +
        "if dst.exists(): raise SystemExit('refuse_to_replace_existing_image')\n" +
        "shutil.copy2(src,dst)\n" +
        "record={'image_path':str(dst),'source_path':str(src),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'source_unchanged':True}\n" +
        "(base/'NATIVE-OBSERVATION.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\\n')\n" +
        "print(json.dumps(record))\nARM2_COPY_PY",
      max_output_tokens: 2000, login: false
    });
    if (copy.exit_code !== 0) throw new Error("Native result persistence failed; do not generate again.");
    const record = JSON.parse(copy.output);
    store("arm2_native_observation", record);
    text({native_image_saved: record.image_path, sha256: record.sha256, actual_call_count: 1});
    return {outcome: "returned", image_path: record.image_path};
  }
  return {adapted, observe};
}
