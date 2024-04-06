'use client';
import { Button } from '@mui/material';
import { create } from '@/actions/actions';

export function TestButton() {
	return (
		<button onClick={() => create()}>Test</button>
	);
}

export function TestButton2({ users }: { users: any }) {
	return (
		<>
			{users}
		</>
	)
}