import { SignedIn, SignedOut, SignInButton } from "@clerk/nextjs";
import RagApp from "../components/RagApp";
export default function Home() {
  return (
    <>
      <SignedOut>
        <div className="flex h-screen items-center justify-center">
          <SignInButton />
        </div>
      </SignedOut>

      <SignedIn>
        <RagApp />
      </SignedIn>
    </>
  );
}
