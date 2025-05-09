import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
    name: "DaniMCP Typescript Server",
    version: "1.0.0"
});

// function to calculate my age from my birthdate
function calculateAge(birthdate: Date): string {
    const today = new Date();
    let age = today.getFullYear() - birthdate.getFullYear();
    const m = today.getMonth() - birthdate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthdate.getDate())) {
        age--;
    }
    return "My age is : " + age;
}


// Add an addition tool
server.tool(
    "about_me", // title
    "description about dani ", // description
    {  
        name: z.string().describe("Daniel Ávila Arias"),
        age: z.number().describe(calculateAge(new Date("1988-01-25"))),
        location: z.string().describe("Grand Rapids, Michigan, USA"),
        occupation: z.string().describe("AI Software Engineer"),
        education: z.string().describe("Computer Science"),
    },
    async ({  }) => ({
      content: [{ 
            type: "text", 
            text: "My name is ${name}, I am ${age} years old, I live in ${location}, I am a ${occupation} and I have a degree in ${education}."
        }]
    })
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
const transport = new StdioServerTransport();
await server.connect(transport);