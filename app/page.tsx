import Image from "next/image";
import { TestButton, TestButton2 } from "@/app/ui/Buttons";
import { getUsers } from "@/actions/actions";

export default function Home() {
  const users = getUsers();
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <TestButton />
      <TestButton2 users={users} />
    </main>
  );
}
