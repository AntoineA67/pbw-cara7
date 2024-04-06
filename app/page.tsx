import Image from "next/image";
import TestButton from "../components/TestButton";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <TestButton />
    </main>
  );
}
