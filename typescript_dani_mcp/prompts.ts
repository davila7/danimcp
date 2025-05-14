import { GetPromptResult } from "@modelcontextprotocol/sdk/types.js";

/**
 * Prompts implementation for Daniel Avila's MCP server
 */
export class DaniMCPPrompts {
  /**
   * Creates a prompt for getting information about Daniel
   */
  async about_me_prompt(): Promise<GetPromptResult> {
    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: "Let me tell you about Daniel Avila:"
          }
        }
      ]
    };
  }

  /**
   * Creates a prompt for technology information
   */
  async tech_prompt(tech?: string): Promise<GetPromptResult> {
    let promptText = "Let's explore Daniel's technical expertise:";
    
    if (tech) {
      promptText += ` Tell me about his experience with ${tech}`;
    }
    
    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: promptText
          }
        }
      ]
    };
  }
}
