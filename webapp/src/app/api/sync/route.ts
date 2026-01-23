import { NextRequest, NextResponse } from "next/server";

// Secret key to protect the endpoint
const SYNC_SECRET = process.env.SYNC_SECRET || "your-secret-key";

export async function POST(request: NextRequest) {
  // Verify authorization
  const authHeader = request.headers.get("authorization");
  if (authHeader !== `Bearer ${SYNC_SECRET}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Note: Actual sync is handled by GitHub Actions
  // This endpoint is for manual trigger notification only
  return NextResponse.json({
    success: true,
    message: "Sync is handled by GitHub Actions. Trigger manually at: https://github.com/delfinparis/keeping-it-real-content-system/actions",
    timestamp: new Date().toISOString(),
  });
}

// GET endpoint to check sync status
export async function GET() {
  return NextResponse.json({
    status: "ok",
    message: "Sync status available at GitHub Actions",
    actionsUrl: "https://github.com/delfinparis/keeping-it-real-content-system/actions",
  });
}
