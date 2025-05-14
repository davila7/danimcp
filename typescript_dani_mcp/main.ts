import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
    name: "DaniMCP Typescript Server",
    version: "1.0.0"
});


// Add an addition tool
server.tool(
    "about_me", // title
    "description about me ", // description
    {
        name: z.string().describe("Name"),
    },
    async ({ name }) => {
        return {
            content: [{
                type: "text",
                text: "My name is ${name}"
            }]
        }
    }
);

// Add a dynamic greeting resource
server.resource(
    "greeting",
    new ResourceTemplate("greeting://{name}", { list: undefined }),
    async (uri, { name }) => ({
        contents: [{
            uri: uri.href,
            text: `Hello, ${name}!`
        }]
    })
);


// Start receiving messages on stdin and sending messages on stdout
// Wrap the connection logic in an async function
async function startServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}
  
// Call the async function
startServer();