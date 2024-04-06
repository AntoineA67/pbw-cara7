'use client';
import { Button } from '@mui/material';
import { create, getUsers } from '@/actions/actions';

export function TestButton() {
	return (
		<button onClick={() => create()}>Test</button>
	);
}

export function TestButton2() {
	const users = getUsers();
	return (
		<>
			{users}
		</>
	)
}