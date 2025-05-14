// File: tools.ts
import { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { TextContent } from "@modelcontextprotocol/sdk/types.js";

/**
 * Tools implementation for Daniel Avila's MCP server
 */
export class DaniMCPTools {
  private _base_url: string;

  constructor() {
    this._base_url = "https://www.danielavila.me/api";
  }

  /**
   * Helper method to fetch data from the API (GET requests)
   */
  private async _fetch_api_data(endpoint: string): Promise<any> {
    try {
      const response = await fetch(`${this._base_url}/${endpoint}`);
      if (response.ok) {
        return await response.json();
      } else {
        throw new Error(`Error: Response code ${response.status}`);
      }
    } catch (e) {
      throw new Error(`Error fetching data from API: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  /**
   * Helper method to post data to the API (POST requests)
   */
  private async _post_api_data(endpoint: string, data: any): Promise<any> {
    try {
      const response = await fetch(`${this._base_url}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        return await response.json();
      } else {
        throw new Error(`Error: Response code ${response.status}`);
      }
    } catch (e) {
      throw new Error(`Error posting data to API: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  /**
   * Formats data for MCP response
   */
  private _format_response(data: any): CallToolResult {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(data, null, 4)
        } as TextContent
      ]
    };
  }

  /**
   * Gets a greeting from the API
   */
  async hello(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("hello");
    return this._format_response(data);
  }

  /**
   * Gets information about Daniel Avila
   */
  async about_me(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("about_me");
    return this._format_response(data);
  }

  /**
   * Gets information about technologies Daniel Avila uses
   */
  async technologies(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("technologies");
    return this._format_response(data);
  }

  /**
   * Gets information about Daniel Avila's projects
   */
  async projects(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("projects");
    return this._format_response(data);
  }

  /**
   * Gets Daniel Avila's contact information
   */
  async contact(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("contact");
    return this._format_response(data);
  }

  /**
   * Sends a message through the contact form
   */
  async send_contact_message(message: string): Promise<CallToolResult> {
    const data = await this._post_api_data("contact", { message });
    return this._format_response(data);
  }

  /**
   * Retrieves information about talks given and community involvement
   */
  async talks(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("talks");
    return this._format_response(data);
  }

  /**
   * Retrieves detailed information about different skill sets
   */
  async skills(): Promise<CallToolResult> {
    const data = await this._fetch_api_data("skills");
    return this._format_response(data);
  }

  /**
   * Checks if Daniel Avila has a specific skill
   */
  async check_skill(skill_name: string): Promise<CallToolResult> {
    const data = await this._fetch_api_data(`skills/${skill_name}`);
    return this._format_response(data);
  }
}
