import {
  agents,
  knowledgeMetrics,
  statusLabels,
  valueProposition,
  workflows,
} from "../lib/mock-data.js";

function renderStatusBadge(status) {
  const label = statusLabels[status] || status;
  return `<span class="workflow-status ${status}">${label}</span>`;
}

export function renderDashboard(root) {
  root.innerHTML = `
    <div class="dashboard">
      <header class="topbar">
        <div class="brand">
          <div class="brand-mark">CB</div>
          <div>
            <h1>${valueProposition.title}</h1>
            <p>${valueProposition.subtitle}</p>
          </div>
        </div>
        <a class="btn-secondary" href="./pages/bridge.html">Bridge Console</a>
      </header>

      <section class="hero">
        <div class="panel hero-copy">
          <h2>Connect company knowledge to agents that execute work.</h2>
          <p>${valueProposition.description}</p>
        </div>
        <div class="panel hero-highlight">
          <div class="highlight-pill">
            <strong>Knowledge layer</strong>
            <span>Docs, wikis, and tools unified into one searchable brain.</span>
          </div>
          <div class="highlight-pill">
            <strong>Workflow layer</strong>
            <span>Every task routed to the right agent with full context.</span>
          </div>
          <div class="highlight-pill">
            <strong>Execution layer</strong>
            <span>Cursor, Claude, and Knowledge agents ship outcomes — not just answers.</span>
          </div>
        </div>
      </section>

      <section>
        <h2 class="section-title">Knowledge Overview</h2>
        <div class="metrics">
          ${knowledgeMetrics
            .map(
              (metric) => `
            <article class="metric-card">
              <div class="metric-top">
                <span class="metric-label">${metric.label}</span>
                <span class="metric-icon">${metric.icon}</span>
              </div>
              <div class="metric-value">${metric.value}</div>
              <div class="metric-change">${metric.change}</div>
            </article>
          `
            )
            .join("")}
        </div>
      </section>

      <section>
        <h2 class="section-title">AI Agents</h2>
        <div class="agents">
          ${agents
            .map(
              (agent) => `
            <article class="agent-card">
              <div class="agent-head">
                <div class="agent-avatar" style="background:${agent.accent}">${agent.initials}</div>
                <div>
                  <h3 class="agent-name">${agent.name}</h3>
                  <p class="agent-role">${agent.role}</p>
                </div>
              </div>
              <p class="agent-description">${agent.description}</p>
              <div class="agent-footer">
                <span class="status-badge ${agent.status}">● Active</span>
                <span class="agent-meta">${agent.tasksToday} tasks today</span>
              </div>
            </article>
          `
            )
            .join("")}
        </div>
      </section>

      <section class="panel workflows-panel">
        <h2 class="section-title">Recent Workflows</h2>
        <table class="workflow-table">
          <thead>
            <tr>
              <th>Workflow</th>
              <th>Agent</th>
              <th>Status</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            ${workflows
              .map(
                (workflow) => `
              <tr>
                <td class="workflow-title">${workflow.title}</td>
                <td>${workflow.agent}</td>
                <td>${renderStatusBadge(workflow.status)}</td>
                <td>${workflow.time}</td>
              </tr>
            `
              )
              .join("")}
          </tbody>
        </table>
      </section>

      <section class="cta-bar">
        <div class="cta-copy">
          <h3>Route work to the right agent in one click.</h3>
          <p>Investors should instantly see knowledge flowing into autonomous execution.</p>
        </div>
        <button class="btn-primary" id="open-task-modal">Send Task to Agent</button>
      </section>

      <p class="footer-note">Demo data only · Company Brain YC demo screen</p>
    </div>

    <div class="modal-backdrop" id="task-modal" aria-hidden="true">
      <div class="modal" role="dialog" aria-modal="true" aria-labelledby="task-modal-title">
        <h3 id="task-modal-title">Send Task to Agent</h3>
        <p>Choose an agent and describe the work. This demo simulates routing with mock data.</p>
        <label for="task-agent">Agent</label>
        <select id="task-agent">
          ${agents.map((agent) => `<option value="${agent.id}">${agent.name}</option>`).join("")}
        </select>
        <label for="task-input">Task</label>
        <textarea id="task-input" placeholder="Example: Update the onboarding SOP with the latest product changes."></textarea>
        <div class="modal-actions">
          <button class="btn-secondary" id="close-task-modal" type="button">Cancel</button>
          <button class="btn-primary" id="submit-task" type="button">Send Task</button>
        </div>
      </div>
    </div>

    <div class="toast" id="task-toast" role="status"></div>
  `;
}

export function bindDashboardInteractions(root) {
  const modal = root.querySelector("#task-modal");
  const toast = root.querySelector("#task-toast");
  const openButton = root.querySelector("#open-task-modal");
  const closeButton = root.querySelector("#close-task-modal");
  const submitButton = root.querySelector("#submit-task");
  const agentSelect = root.querySelector("#task-agent");
  const taskInput = root.querySelector("#task-input");

  const showToast = (message) => {
    toast.textContent = message;
    toast.classList.add("show");
    window.setTimeout(() => toast.classList.remove("show"), 3200);
  };

  const openModal = () => {
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    taskInput.focus();
  };

  const closeModal = () => {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  };

  openButton.addEventListener("click", openModal);
  closeButton.addEventListener("click", closeModal);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });

  submitButton.addEventListener("click", () => {
    const agent = agents.find((item) => item.id === agentSelect.value);
    const task = taskInput.value.trim() || "Untitled demo task";
    closeModal();
    showToast(`Task sent to ${agent.name}: "${task}"`);
    taskInput.value = "";
  });
}
