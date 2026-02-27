import { NextResponse } from "next/server";
import { exec } from "child_process";
import { promisify } from "util";
import path from "path";

const execAsync = promisify(exec);

export async function POST() {
  try {
    const crawlerDir = path.join(process.cwd(), "crawler");
    const { stdout, stderr } = await execAsync(
      "python summarizer.py",
      { cwd: crawlerDir, timeout: 90000 }
    );

    if (stderr) {
      console.error("[Summary] stderr:", stderr);
    }

    const result = JSON.parse(stdout.trim());
    return NextResponse.json(result);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
