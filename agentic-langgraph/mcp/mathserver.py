from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")
@mcp.tool()
def add(a:int,b:int)->int:
    """Add to numbers"""
    return a+b

def multiple(a:int, b:int)->int:
    """Multiply two numbers"""
    return a*b

# The transport ="stdio" argument tell the server to:
# Use standard input/output(stdin and stdout) to receive and respond to tool function calls

if __name__=="__main__":
    mcp.run(transport="stdio")