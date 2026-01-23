import { NextRequest, NextResponse } from "next/server";
import { spawn } from "child_process";
import path from "path";

// Secret key to protect the endpoint
const SYNC_SECRET = process.env.SYNC_SECRET || "your-secret-key";

export async function POST(request: NextRequest) {
  // Verify authorization
  const authHeader = request.headers.get("authorization");
  if (authHeader !== `Bearer ${SYNC_SECRET}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    // Path to the auto_sync script
    const projectRoot = path.resolve(process.cwd(), "..");
    const scriptPath = path.join(projectRoot, "scripts", "auto_sync.py");
    const pythonPath = path.join(projectRoot, "venv", "bin", "python");

    // Run the sync script
    const syncProcess = spawn(pythonPath, [scriptPath], {
      cwd: projectRoot,
      env: {
        ...process.env,
        OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
      },
    });

    // Collect output
    let stdout = "";
    let stderr = "";

    syncProcess.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    syncProcess.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    // Wait for completion (with timeout)
    const result = await new Promise<{ success: boolean; output: string }>((resolve) => {
      const timeout = setTimeout(() => {
        syncProcess.kill();
        resolve({ success: false, output: "Sync timed out after 30 minutes" });
      }, 30 * 60 * 1000); // 30 minute timeout

      syncProcess.on("close", (code) => {
        clearTimeout(timeout);
        resolve({
          success: code === 0,
          output: stdout + stderr,
        });
      });
    });

    return NextResponse.json({
      success: result.success,
      message: result.success ? "Sync completed successfully" : "Sync failed",
      output: result.output.slice(-2000), // Last 2000 chars
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Sync error:", error);
    return NextResponse.json(
      { error: "Sync failed", details: String(error) },
      { status: 500 }
    );
  }
}

// GET endpoint to check sync status
export async function GET() {
  try {
    // Read progress.json to get current status
    const fs = await import("fs/promises");
    const path = await import("path");
    const projectRoot = path.resolve(process.cwd(), "..");
    const progressPath = path.join(projectRoot, "data", "index", "progress.json");

    const progressData = await fs.readFile(progressPath, "utf-8");
    const progress = JSON.parse(progressData);

    return NextResponse.json({
      status: "ok",
      progress,
      lastSync: progress.last_analysis || "unknown",
    });
  } catch {
    return NextResponse.json({
      status: "ok",
      progress: { downloaded: 0, transcribed: 0, analyzed: 0 },
      lastSync: "never",
    });
  }
}
