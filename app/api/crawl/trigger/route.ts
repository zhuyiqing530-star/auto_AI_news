import { NextResponse } from "next/server";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

export async function POST() {
  try {
    const cwd = process.cwd();
    execAsync(`python "${cwd}/crawler/main.py" --once`, {
      cwd,
      timeout: 300000,
    });

    return NextResponse.json({ status: "crawl_started" });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to start crawl" },
      { status: 500 }
    );
  }
}
