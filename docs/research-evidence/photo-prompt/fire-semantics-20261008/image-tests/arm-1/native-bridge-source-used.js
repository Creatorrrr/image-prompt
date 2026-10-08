
async function runPhotoNative({tools, run, workflowScript, python, ledger, observe}) {
  const quote = s => "'" + String(s).replaceAll("'", "'\\''") + "'";
  async function command(argv) {
    const answer = await tools.exec_command({cmd: argv.map(quote).join(" "), max_output_tokens: 2000});
    if (answer.exit_code !== 0) throw new Error("native_bridge_command_failed");
    return JSON.parse(answer.output);
  }
  const started = await command([python, workflowScript, "native-started", "--run", run]);
  let result;
  try {
    result = await tools.image_gen__imagegen(started.payload);
  } catch (error) {
    const capture = {type: error?.name || typeof error, message: String(error)};
    await command([python, workflowScript.replace(/photo_workflow\.py$/, "photo_native_bridge.py"),
      "observe", "--run", run, "--ledger", ledger, "--error-json", JSON.stringify(capture)]);
    return {outcome: "tool_error", operation_id: started.operation_id};
  }
  if (result?.isError === true) {
    await command([python, workflowScript.replace(/photo_workflow\.py$/, "photo_native_bridge.py"),
      "observe", "--run", run, "--ledger", ledger, "--error-json", JSON.stringify(result)]);
  } else {
    const observed = await observe(result);
    await command([python, workflowScript.replace(/photo_workflow\.py$/, "photo_native_bridge.py"),
      "observe", "--run", run, "--ledger", ledger, "--observation-json", JSON.stringify({operation_id: started.operation_id, ...observed})]);
  }
  return result;
}

