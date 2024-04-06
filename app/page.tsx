import Image from "next/image";
import { TestButton, TestButton2 } from "@/app/ui/Buttons";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <TestButton />
      <TestButton2 />
    </main>
  );
}
