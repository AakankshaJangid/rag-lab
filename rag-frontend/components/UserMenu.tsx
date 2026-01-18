"use client";

import { SignOutButton, useUser } from "@clerk/nextjs";

export default function UserMenu() {
  const { user, isLoaded } = useUser();

  if (!isLoaded) return null;
  if (!user) return null;

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-gray-600">
        Hello, {user.fullName || user.username || user.primaryEmailAddress?.emailAddress}
      </span>

      <SignOutButton>
        <button className="px-3 py-1 rounded-md bg-orange-600 text-white hover:bg-orange-700 transition">
          Sign out
        </button>
      </SignOutButton>
    </div>
  );
}
