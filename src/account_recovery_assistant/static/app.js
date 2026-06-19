const statusNode = document.querySelector("#status");
const wizardNode = document.querySelector("#wizard");
let currentPlanPayload = null;
let currentPlan = null;

async function fetchJson(path, options = {}) {
  const response = await fetch(path, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = payload.detail || payload.error || `Request failed: ${response.status}`;
    const error = new Error(detail);
    error.field = payload.field;
    throw error;
  }
  return payload;
}

async function fetchText(path, options = {}) {
  const response = await fetch(path, options);
  const body = await response.text();
  if (!response.ok) {
    throw new Error(body || `Request failed: ${response.status}`);
  }
  return body;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderIncidentPicker(incidents) {
  statusNode.textContent = "Choose the incident that best matches the recovery problem.";
  wizardNode.innerHTML = `
    <section class="stack">
      <section>
        <h2>Pick Your Incident</h2>
        <p class="warning">Do not enter passwords, backup codes, SMS codes, or authenticator codes into this wizard.</p>
        <div class="incident-grid">
          ${incidents
            .map(
              (incident) => `
                <button class="incident-card" data-incident-id="${incident.id}">
                  <h3>${escapeHtml(incident.title)}</h3>
                  <p class="muted">${escapeHtml(incident.service)}</p>
                </button>
              `,
            )
            .join("")}
        </div>
      </section>
    </section>
  `;

  for (const button of wizardNode.querySelectorAll("[data-incident-id]")) {
    button.addEventListener("click", async () => {
      await loadQuestionnaire(button.getAttribute("data-incident-id"));
    });
  }
}

function renderQuestion(question) {
  const yesNoChoices =
    question.answer_type === "boolean"
      ? `
        <label><input type="radio" name="${question.field}" value="true" required> Yes</label>
        <label><input type="radio" name="${question.field}" value="false" required> No</label>
      `
      : question.choices
          .map(
            (choice) => `
              <label><input type="radio" name="${question.field}" value="${escapeHtml(choice.value)}" required> ${escapeHtml(choice.label)}</label>
            `,
          )
          .join("");

  return `
    <section class="question">
      <h3>${escapeHtml(question.prompt)}</h3>
      <div class="choice-group">${yesNoChoices}</div>
    </section>
  `;
}

async function loadQuestionnaire(incidentId) {
  try {
    statusNode.textContent = "Loading questionnaire...";
    const payload = await fetchJson(`/api/incidents/${incidentId}/questionnaire`);
    statusNode.textContent = `Answer the questions for ${payload.title}.`;
    wizardNode.innerHTML = `
      <section class="stack">
        <section>
          <h2>${escapeHtml(payload.title)}</h2>
          <p class="muted">${escapeHtml(payload.service)}</p>
          <p class="warning">Use this wizard for guidance only. Do not paste passwords, backup codes, or identity document numbers here.</p>
          <form id="questionnaire-form">
            ${payload.questions.map(renderQuestion).join("")}
            <div class="actions">
              <button type="submit">Generate Recovery Plan</button>
              <button type="button" class="secondary" id="back-button">Back</button>
            </div>
          </form>
        </section>
      </section>
    `;

    wizardNode.querySelector("#back-button").addEventListener("click", init);
    wizardNode.querySelector("#questionnaire-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(event.currentTarget);
      const answers = Object.fromEntries(formData.entries());
      const payloadBody = { incident_id: incidentId, service: payload.service };

      for (const [key, value] of Object.entries(answers)) {
        payloadBody[key] = value === "true" ? true : value === "false" ? false : value;
      }

      await submitPlan(payloadBody);
    });
  } catch (error) {
    renderError("Questionnaire unavailable", error.message);
  }
}

function listHtml(items, render = (item) => escapeHtml(item)) {
  return `<ul>${items.map((item) => `<li>${render(item)}</li>`).join("")}</ul>`;
}

function markdownList(items = []) {
  return items.map((item) => `- ${item}`).join("\n");
}

function markdownLinks(items = []) {
  return items.map((item) => `- [${item.label}](${item.url})`).join("\n");
}

function knowledgeFreshnessMarkdown(knowledgeBase) {
  if (!knowledgeBase) {
    return "- Last verified: Unknown\n- Review due: Unknown\n- Review cadence: Unknown days\n- Confidence: unknown\n- Status: unknown\n- Stale: unknown";
  }
  return markdownList([
    `Last verified: ${knowledgeBase.last_verified_at || "Unknown"}`,
    `Review due: ${knowledgeBase.review_due_at || "Unknown"}`,
    `Review cadence: ${knowledgeBase.review_cadence_days || "Unknown"} days`,
    `Confidence: ${knowledgeBase.confidence}`,
    `Status: ${knowledgeBase.status}`,
    `Stale: ${knowledgeBase.stale ? "yes" : "no"}`,
  ]);
}

function planToMarkdown(plan) {
  return [
    "# Account Recovery Plan",
    "",
    `Service: ${plan.service}`,
    `Case type: ${plan.case_type}`,
    `Incident: ${plan.incident_title || "General recovery case"}`,
    `Decision path: ${plan.decision_path_id || "unknown"}`,
    "",
    "## Next Best Action",
    "",
    plan.next_best_action,
    "",
    "## Prepare Now",
    "",
    markdownList(plan.prepare_now),
    "",
    "## What Can Make This Worse",
    "",
    markdownList(plan.what_can_make_this_worse),
    "",
    "## Escalate When",
    "",
    markdownList(plan.escalate_when),
    "",
    `Expected timeline: ${plan.expected_timeline}`,
    "",
    "## Checklist",
    "",
    markdownList(plan.checklist),
    "",
    "## Evidence To Prepare",
    "",
    markdownList(plan.evidence),
    "",
    "## Official Links",
    "",
    markdownLinks(plan.official_links),
    "",
    "## Knowledge Freshness",
    "",
    knowledgeFreshnessMarkdown(plan.knowledge_base),
    "",
    "## Common Mistakes To Avoid",
    "",
    markdownList(plan.common_mistakes),
    "",
    "## Support Message",
    "",
    plan.support_message,
    "",
    "## Source Notes",
    "",
    markdownList(plan.source_notes),
    "",
    "## Post-Recovery Hardening",
    "",
    markdownList(plan.hardening_steps),
    "",
    "## Safety Warnings",
    "",
    markdownList(plan.safety_warnings),
    "",
  ].join("\n");
}

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function markdownFromServerOrFallback() {
  const payload = currentPlanPayload;
  if (!payload) {
    return planToMarkdown(currentPlan);
  }
  return fetchText("/api/plan/markdown", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

async function downloadMarkdownFromServer() {
  const markdown = await markdownFromServerOrFallback();
  downloadText("account-recovery-plan.md", markdown);
}

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  document.execCommand("copy");
  textArea.remove();
}

function renderPlan(plan) {
  const warning =
    plan.knowledge_base && plan.knowledge_base.status !== "verified"
      ? `<div class="warning">This incident record is marked ${escapeHtml(plan.knowledge_base.status)}. Re-check the official flow before relying on service-specific details.</div>`
      : "";

  if (!plan.allowed) {
    statusNode.textContent = "Safety refusal";
    wizardNode.innerHTML = `
      <section class="stack">
        <section class="warning">
          <h2>Request Not Supported</h2>
          <p>${escapeHtml(plan.reason)}</p>
        </section>
      </section>
    `;
    return;
  }

  statusNode.textContent = "Review the recovery plan and follow official channels only.";
  wizardNode.innerHTML = `
    <section class="stack">
      ${warning}
      <section class="plan-section">
        <p class="muted">Step 3 of 3 · recovery plan ready.</p>
        <div class="progress" aria-label="Wizard progress"><span style="width: 100%"></span></div>
        <h2>${escapeHtml(plan.incident_title || "Recovery Plan")}</h2>
        <p class="muted">${escapeHtml(plan.service)} · ${escapeHtml(plan.case_type)}</p>
      </section>
      <section class="plan-section">
        <h3>Next Best Action</h3>
        <p>${escapeHtml(plan.next_best_action)}</p>
      </section>
      <section class="plan-section">
        <h3>Prepare Now</h3>
        ${listHtml(plan.prepare_now)}
      </section>
      <section class="plan-section">
        <h3>What Can Make This Worse</h3>
        ${listHtml(plan.what_can_make_this_worse)}
      </section>
      <section class="plan-section">
        <h3>Escalate When</h3>
        ${listHtml(plan.escalate_when)}
      </section>
      <section class="plan-section">
        <h3>Expected Timeline</h3>
        <p>${escapeHtml(plan.expected_timeline)}</p>
      </section>
      <section class="plan-section">
        <h3>Checklist</h3>
        ${listHtml(plan.checklist)}
      </section>
      <section class="plan-section">
        <h3>Evidence To Prepare</h3>
        ${listHtml(plan.evidence)}
      </section>
      <section class="plan-section">
        <h3>Official Links</h3>
        ${listHtml(plan.official_links, (item) => `<a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.label)}</a>`)}
      </section>
      <section class="plan-section">
        <h3>Support Message</h3>
        <p>${escapeHtml(plan.support_message)}</p>
      </section>
      <section class="plan-section">
        <h3>Knowledge Freshness</h3>
        ${listHtml([
          `Last verified: ${plan.knowledge_base.last_verified_at || "Unknown"}`,
          `Review due: ${plan.knowledge_base.review_due_at || "Unknown"}`,
          `Confidence: ${plan.knowledge_base.confidence}`,
          `Status: ${plan.knowledge_base.status}`,
        ])}
      </section>
      <section class="plan-section">
        <h3>Post-Recovery Hardening</h3>
        ${listHtml(plan.hardening_steps)}
      </section>
      <section class="plan-section">
        <h3>Safety Warnings</h3>
        ${listHtml(plan.safety_warnings)}
      </section>
      <section class="plan-section">
        <h3>Feedback</h3>
        <p class="muted">Optional: send minimal, memory-only feedback to this local server for the current session. Do not include personal details.</p>
        <label class="consent"><input type="checkbox" id="feedback-consent"> I consent to share this minimal outcome for this local session.</label>
        <div class="actions">
          <button type="button" id="feedback-recovered">I recovered access</button>
          <button type="button" id="feedback-stuck">I'm still stuck</button>
          <button type="button" id="feedback-link-worked">Official link worked</button>
          <button type="button" id="feedback-link-failed">Official link didn't work</button>
        </div>
      </section>
      <div class="actions">
        <button type="button" id="copy-support-message">Copy Support Message</button>
        <button type="button" id="copy-full-plan">Copy Full Plan</button>
        <button type="button" id="download-markdown">Download Markdown</button>
        <button type="button" id="print-plan">Print Plan</button>
        <button type="button" class="secondary" id="start-over">Start Over</button>
      </div>
    </section>
  `;

  wizardNode.querySelector("#copy-support-message").addEventListener("click", async () => {
    await copyText(plan.support_message);
    statusNode.textContent = "Support message copied.";
  });
  wizardNode.querySelector("#copy-full-plan").addEventListener("click", async () => {
    try {
      await copyText(await markdownFromServerOrFallback());
      statusNode.textContent = "Full plan copied.";
    } catch (error) {
      await copyText(planToMarkdown(plan));
      statusNode.textContent = "Full plan copied from browser fallback.";
    }
  });
  wizardNode.querySelector("#print-plan").addEventListener("click", () => {
    window.print();
  });
  wizardNode.querySelector("#download-markdown").addEventListener("click", async () => {
    try {
      await downloadMarkdownFromServer();
    } catch (error) {
      downloadText("account-recovery-plan.md", planToMarkdown(plan));
      statusNode.textContent = "Downloaded fallback Markdown from the browser.";
    }
  });
  wizardNode.querySelector("#feedback-recovered").addEventListener("click", () => submitFeedback("recovered", "not_used"));
  wizardNode.querySelector("#feedback-stuck").addEventListener("click", () => submitFeedback("stuck", "not_used"));
  wizardNode.querySelector("#feedback-link-worked").addEventListener("click", () => submitFeedback("stuck", "worked"));
  wizardNode.querySelector("#feedback-link-failed").addEventListener("click", () => submitFeedback("stuck", "failed"));
  wizardNode.querySelector("#start-over").addEventListener("click", init);
}

async function submitPlan(payload) {
  try {
    statusNode.textContent = "Generating plan...";
    const plan = await fetchJson("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    currentPlanPayload = payload;
    currentPlan = plan;
    renderPlan(plan);
  } catch (error) {
    renderError("Could not generate a plan", error.message);
  }
}

async function submitFeedback(outcome, linkStatus) {
  const consent = Boolean(wizardNode.querySelector("#feedback-consent")?.checked);
  if (!consent) {
    statusNode.textContent = "Feedback not sent: consent checkbox is required.";
    return;
  }
  try {
    const payload = {
      consent,
      outcome,
      link_status: linkStatus,
      incident_id: currentPlan?.incident_id,
      decision_path_id: currentPlan?.decision_path_id,
    };
    await fetchJson("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    statusNode.textContent = "Feedback sent to the local session only.";
  } catch (error) {
    renderError("Could not submit feedback", error.message);
  }
}

async function init() {
  try {
    statusNode.textContent = "Loading incidents...";
    const payload = await fetchJson("/api/incidents");
    renderIncidentPicker(payload.incidents);
  } catch (error) {
    renderError("Could not load incidents", error.message);
  }
}

function renderError(title, detail) {
  statusNode.textContent = "Error";
  wizardNode.innerHTML = `
    <section class="stack">
      <section class="warning">
        <h2>${escapeHtml(title)}</h2>
        <p>${escapeHtml(detail)}</p>
      </section>
      <div class="actions">
        <button type="button" id="retry-button">Try Again</button>
      </div>
    </section>
  `;
  wizardNode.querySelector("#retry-button").addEventListener("click", init);
}

void init();
