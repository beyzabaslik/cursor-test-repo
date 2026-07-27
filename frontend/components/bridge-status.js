/**
 * Render bridge status cards into the demo dashboard.
 * @param {HTMLElement} root
 * @param {import('../lib/cursor-bridge.js').CursorBridgeClient} client
 */
export async function renderBridgeStatus(root, client) {
  const [health, status, tools] = await Promise.all([
    client.getHealth(),
    client.getStatus(),
    client.listTools(),
  ]);

  root.innerHTML = `
    <section class="card">
      <h2>Bridge Health</h2>
      <p><strong>Status:</strong> ${health.status}</p>
      <p><strong>Provider:</strong> ${health.provider}</p>
      <p><strong>Backend:</strong> ${health.backend}</p>
      <p>${health.message}</p>
    </section>
    <section class="card">
      <h2>MCP Tools</h2>
      <ul>${(tools.tools || [])
        .map((tool) => `<li><code>${tool.name}</code> — ${tool.description || ""}</li>`)
        .join("")}</ul>
      <p><strong>Connected tools:</strong> ${(status.tools || []).join(", ") || "none"}</p>
    </section>
  `;
}
