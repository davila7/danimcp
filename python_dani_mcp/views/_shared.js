// Shared bootstrap for DaniMCP views — inlined by views.py into each view's module script.
import {
  App,
  applyDocumentTheme,
  applyHostFonts,
  applyHostStyleVariables,
} from "https://cdn.jsdelivr.net/npm/@modelcontextprotocol/ext-apps@2.0.4/dist/src/app-with-deps.js";

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (c) => ESCAPES[c]);
const $ = (id) => document.getElementById(id);

/** Only allow http(s) links coming from API data. */
function safeUrl(url) {
  try {
    const parsed = new URL(url);
    return parsed.protocol === "https:" || parsed.protocol === "http:" ? parsed.href : null;
  } catch {
    return null;
  }
}

function setStatus(text, isError = false) {
  const el = $("status");
  el.textContent = text;
  el.classList.toggle("error", isError);
  el.hidden = false;
}

function applyHostContext(ctx) {
  if (!ctx) return;
  if (ctx.theme) applyDocumentTheme(ctx.theme);
  if (ctx.styles?.variables) applyHostStyleVariables(ctx.styles.variables);
  if (ctx.styles?.css?.fonts) applyHostFonts(ctx.styles.css.fonts);
}

function textOf(result) {
  return result.content?.find((c) => c.type === "text")?.text;
}

function dataOf(result) {
  if (result.structuredContent) return result.structuredContent;
  const text = textOf(result);
  return text ? JSON.parse(text) : null;
}

/**
 * Connect to the host and call `render(data, app)` with the tool's structuredContent.
 * Handlers are registered before connect() so the one-shot tool-result notification is not missed.
 */
async function mountView(name, render) {
  const app = new App({ name, version: "2.0.0" });

  app.ontoolresult = (result) => {
    if (result.isError) {
      setStatus(textOf(result) || "The tool returned an error.", true);
      return;
    }
    try {
      const data = dataOf(result);
      if (!data) throw new Error("empty tool result");
      $("status").hidden = true;
      render(data, app);
    } catch (err) {
      setStatus(`Could not render the result: ${err.message}`, true);
    }
  };
  app.ontoolcancelled = () => setStatus("The tool call was cancelled.", true);
  app.onhostcontextchanged = applyHostContext;

  // Links in a sandboxed iframe must go through the host.
  document.addEventListener("click", (event) => {
    const link = event.target.closest?.("a[href]");
    if (!link) return;
    event.preventDefault();
    app.openLink({ url: link.href }).catch(() => window.open(link.href, "_blank", "noopener"));
  });

  try {
    await app.connect();
    applyHostContext(app.getHostContext());
  } catch (err) {
    setStatus(`Could not connect to the host: ${err.message}`, true);
  }
  return app;
}
