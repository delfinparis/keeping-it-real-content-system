import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  try {
    const problemMapPath = path.join(
      process.cwd(),
      "..",
      "content",
      "problem-map",
      "problem_episode_map.json"
    );

    if (fs.existsSync(problemMapPath)) {
      const data = JSON.parse(fs.readFileSync(problemMapPath, "utf-8"));
      return NextResponse.json(data);
    }

    // Fallback to data directory if not in parent
    const altPath = path.join(
      process.cwd(),
      "src",
      "data",
      "problem_episode_map.json"
    );

    if (fs.existsSync(altPath)) {
      const data = JSON.parse(fs.readFileSync(altPath, "utf-8"));
      return NextResponse.json(data);
    }

    return NextResponse.json({});
  } catch (error) {
    console.error("Error loading problem map:", error);
    return NextResponse.json({});
  }
}
