/**
 * Lightweight client for the local Cursor Bridge endpoints.
 */
export class CursorBridgeClient {
  /**
   * @param {object} options
   * @param {string} [options.baseUrl]
   * @param {string} [options.apiKey]
   */
  constructor({ baseUrl = "/api/cursor-bridge", apiKey = "sk-curbr-local-dev" } = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.apiKey = apiKey;
  }

  authHeaders() {
    return {
      Authorization: `Bearer ${this.apiKey}`,
      "Content-Type": "application/json",
    };
  }

  async getHealth() {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }

  async getStatus() {
    const response = await fetch(`${this.baseUrl}/status`);
    return response.json();
  }

  async listTools() {
    const response = await fetch(`${this.baseUrl}/tools`);
    return response.json();
  }

  async callTool(name, args = {}) {
    const response = await fetch(`${this.baseUrl}/tools/call`, {
      method: "POST",
      headers: this.authHeaders(),
      body: JSON.stringify({ name, arguments: args }),
    });
    return response.json();
  }

  async chat(message, model = "cursor-fast") {
    const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: this.authHeaders(),
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: message }],
      }),
    });
    return response.json();
  }
}
