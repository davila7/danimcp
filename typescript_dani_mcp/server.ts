// File: server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { DaniMCPTools } from "./tools.js";
import { DaniMCPPrompts } from "./prompts.js";

/**
 * Main class for Daniel Avila's MCP server
 */
export class DaniMCPServer {
  private name: string;
  private mcp: McpServer;
  private tools: DaniMCPTools;
  private prompts: DaniMCPPrompts;

  constructor(name: string = "DaniMCP TypeScript Server") {
    this.name = name;
    this.mcp = new McpServer({
      name: this.name,
      version: "1.0.0"
    });
    this.tools = new DaniMCPTools();
    this.prompts = new DaniMCPPrompts();
    this._registerTools();
    this._registerPrompts();
  }

  /**
   * Registers all available tools in the MCP server
   */
  private _registerTools(): void {
    // Register hello tool
    this.mcp.tool(
      "hello",
      "Get a greeting",
      async () => this.tools.hello()
    );

    // Register about_me tool
    this.mcp.tool(
      "about_me",
      "Get information about Daniel Avila",
      async () => this.tools.about_me()
    );

    // Register technologies tool
    this.mcp.tool(
      "technologies",
      "Get information about technologies Daniel Avila uses",
      async () => this.tools.technologies()
    );

    // Register projects tool
    this.mcp.tool(
      "projects",
      "Get information about Daniel Avila's projects",
      async () => this.tools.projects()
    );

    // Register contact tool
    this.mcp.tool(
      "contact",
      "Get Daniel Avila's contact information",
      async () => this.tools.contact()
    );

    // Register send_contact_message tool
    this.mcp.tool(
      "send_contact_message",
      "Send a message through the contact form",
      {
        message: z.string().describe("Message to send")
      },
      async ({ message }) => this.tools.send_contact_message(message)
    );

    // Register talks tool
    this.mcp.tool(
      "talks",
      "Get information about talks given and community involvement",
      async () => this.tools.talks()
    );

    // Register skills tool
    this.mcp.tool(
      "skills",
      "Get detailed information about different skill sets",
      async () => this.tools.skills()
    );

    // Register check_skill tool
    this.mcp.tool(
      "check_skill",
      "Check if Daniel Avila has a specific skill",
      {
        skill_name: z.string().describe("Name of the skill to check")
      },
      async ({ skill_name }) => this.tools.check_skill(skill_name)
    );
  }

  /**
   * Registers all available prompts in the MCP server
   */
  private _registerPrompts(): void {
    // Register about_me_prompt
    this.mcp.prompt(
      "about_me_prompt",
      "A prompt about Daniel Avila",
      async () => this.prompts.about_me_prompt()
    );

    // Register tech_prompt
    this.mcp.prompt(
      "tech_prompt",
      "A prompt about Daniel's technical expertise",
      {
        tech: z.string().optional().describe("Technology to focus on")
      },
      async ({ tech }) => this.prompts.tech_prompt(tech)
    );
  }

  /**
   * Runs the MCP server with the specified transport
   */
  async run(transport: string = "stdio"): Promise<void> {
    if (transport === "stdio") {
      const stdioTransport = new StdioServerTransport();
      await this.mcp.connect(stdioTransport);
    } else {
      throw new Error(`Unsupported transport: ${transport}`);
    }
  }
}

// Create a server instance at the module level
export const server = new DaniMCPServer();

// Main entry point
if (require.main === module) {
  server.run().catch(error => {
    console.error("Server error:", error);
    process.exit(1);
  });
}
