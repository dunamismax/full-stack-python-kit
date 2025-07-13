'use client';

import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { 
  Add as AddIcon,
  Task as TaskIcon,
  Note as NoteIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon 
} from '@mui/icons-material';
import Link from 'next/link';

const actions = [
  {
    title: 'New Task',
    description: 'Create a new task',
    icon: <TaskIcon />,
    href: '/tasks/new',
    color: 'bg-blue-600 hover:bg-blue-700',
  },
  {
    title: 'New Note',
    description: 'Write a new note',
    icon: <NoteIcon />,
    href: '/notes/new',
    color: 'bg-green-600 hover:bg-green-700',
  },
  {
    title: 'View Dashboard',
    description: 'Go to main dashboard',
    icon: <DashboardIcon />,
    href: '/dashboard',
    color: 'bg-purple-600 hover:bg-purple-700',
  },
  {
    title: 'Settings',
    description: 'Manage your account',
    icon: <SettingsIcon />,
    href: '/settings',
    color: 'bg-gray-600 hover:bg-gray-700',
  },
];

export function QuickActions() {
  return (
    <Card>
      <CardContent className="p-6">
        <Typography variant="h6" className="mb-4 text-white font-semibold">
          Quick Actions
        </Typography>
        
        <Box className="space-y-3">
          {actions.map((action, index) => (
            <Button
              key={index}
              component={Link}
              href={action.href}
              variant="contained"
              fullWidth
              startIcon={action.icon}
              className={`${action.color} text-white normal-case justify-start p-3`}
            >
              <Box className="text-left">
                <Typography variant="body1" className="font-medium">
                  {action.title}
                </Typography>
                <Typography variant="caption" className="text-gray-200">
                  {action.description}
                </Typography>
              </Box>
            </Button>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
}