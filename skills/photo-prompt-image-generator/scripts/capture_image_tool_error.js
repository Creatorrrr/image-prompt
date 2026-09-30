// A pure function expression: evaluate this exact file in native code-mode or Node.
// It never invokes an image tool, evaluates a thrown object's getters, or writes files.
(function captureImageToolError(thrown, context = {}) {
  const limitations = [];
  const seen = new WeakMap();
  const own = (value, key) => {
    try { const d = Object.getOwnPropertyDescriptor(value, key); return d && "value" in d ? d.value : undefined; }
    catch (_) { return undefined; }
  };
  function typed(value, depth = 0) {
    if (value === null || typeof value === "string" || typeof value === "boolean") return value;
    if (typeof value === "number") return Number.isFinite(value) ? value : { type: "number", value: String(value) };
    if (typeof value === "undefined" || typeof value === "bigint" || typeof value === "symbol") return { type: typeof value, value: typeof value === "undefined" ? null : String(value) };
    if (depth > 8) { limitations.push("depth_limit"); return { type: typeof value, omitted: true }; }
    if (seen.has(value)) return { type: "reference", id: seen.get(value) };
    seen.set(value, typed.nextId++);
    const result = { type: typeof value, id: seen.get(value), properties: Object.create(null) };
    try {
      const descriptors = Object.getOwnPropertyDescriptors(value);
      const keys = Reflect.ownKeys(descriptors);
      if (keys.length > 128) limitations.push("property_limit");
      for (const key of keys.slice(0, 128)) {
        const descriptor = descriptors[key];
        let label = typeof key === "symbol" ? "[symbol]" + String(key) : key;
        if (Object.hasOwn(result.properties, label)) {
          limitations.push("property_label_collision");
          while (Object.hasOwn(result.properties, label)) label += "#";
        }
        if ("value" in descriptor) result.properties[label] = typed(descriptor.value, depth + 1);
        else { limitations.push("accessor_not_evaluated"); result.properties[label] = { type: "accessor", omitted: true }; }
      }
    } catch (_) { limitations.push("property_capture_failed"); }
    return result;
  }
  typed.nextId = 1;
  const kind = thrown === null ? "null" : typeof thrown;
  const value = typed(thrown);
  const raw = { kind, fidelity: kind === "string" ? "exact_string" : limitations.length ? "limited_capture" : "typed_capture", value, limitations: [...new Set(limitations)] };
  let provider, text = typeof thrown === "string" ? thrown : own(thrown, "message");
  text = typeof text === "string" ? text : "";
  try {
    const wrapper = /Some\(([\s\S]*)\)\s*$/.exec(text);
    provider = JSON.parse(wrapper ? wrapper[1] : text);
    for (let i = 0; i < 2 && typeof provider === "string"; i++) provider = JSON.parse(provider);
  } catch (_) { provider = thrown; }
  provider = own(provider, "error") || provider;
  const str = (object, key) => { const value = own(object, key); return typeof value === "string" ? value : null; };
  const code = str(provider, "code");
  const moderation = own(provider, "moderation_details");
  const categoryValue = own(moderation, "categories");
  let categories = [];
  try {
    if (Array.isArray(categoryValue)) {
      const length = own(categoryValue, "length");
      for (let i = 0; i < Math.min(length, 128); i++) {
        const category = own(categoryValue, String(i));
        if (typeof category === "string") categories.push(category);
      }
      if (length > 128) raw.limitations.push("category_limit");
    }
  } catch (_) {}
  const providerMessage = str(provider, "message") || "";
  const messageId = /request ID ([A-Za-z0-9_-]+)/.exec(providerMessage);
  const bodyId = str(provider, "request_id");
  const blocked = code === "moderation_blocked" || code === "content_policy_violation";
  const http = /\bhttp\s+(\d{3})\b/i.exec(text);
  const display = Array.from((text || providerMessage || "Image tool threw " + kind).replace(/\n/g, " ")).slice(0, 280).map(character => {
    const point = character.codePointAt(0);
    if (point >= 0xD800 && point <= 0xDFFF) {
      raw.limitations.push("display_surrogate_replacement");
      return "\uFFFD";
    }
    return character;
  }).join("");
  raw.limitations = [...new Set(raw.limitations)];
  if (kind !== "string" && raw.limitations.length) raw.fidelity = "limited_capture";
  return {
    contract_version: "photo-image-attempt-evidence/v1",
    tool: context.tool,
    generation_environment: context.generation_environment,
    attempt: context.attempt,
    started_at: context.started_at || null,
    ended_at: context.ended_at || null,
    invocation_outcome: context.invocation_outcome === "returned" ? "returned" : "rejected",
    request: { prompt_en: context.prompt_en, negative_en: context.negative_en ?? null, runtime_prompt_en: context.runtime_prompt_en },
    outcome: {
      status: blocked ? "safety_block" : "error",
      display_message: display,
      http_status: http ? Number(http[1]) : null,
      error_code: code,
      error_type: str(provider, "type"),
      request_id: bodyId || (messageId ? messageId[1] : null),
      request_id_source: bodyId ? "error.request_id" : messageId ? "error.message" : null,
      moderation_stage: str(moderation, "moderation_stage"),
      categories,
      classification_source: blocked ? "structured_error_code" : "unclassified"
    },
    raw_error: raw
  };
})
