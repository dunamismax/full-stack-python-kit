'use client';

import { useEffect } from 'react';
import { Container, Grid, Typography, Box, Card, CardContent, Button } from '@mui/material';
import { 
  Dashboard as DashboardIcon,
  Code as CodeIcon,
  Web as WebIcon,
  DesktopWindows as DesktopIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  CloudSync as CloudIcon,
  Analytics as AnalyticsIcon 
} from '@mui/icons-material';
import Link from 'next/link';

import { useAuth } from '@/lib/auth';
import { DashboardStats } from '@/components/dashboard/DashboardStats';
import { RecentActivity } from '@/components/dashboard/RecentActivity';
import { QuickActions } from '@/components/dashboard/QuickActions';

const features = [
  {
    icon: <CodeIcon sx={{ fontSize: 40 }} />,
    title: 'CLI Tools',
    description: 'Powerful command-line utilities built with Typer and Rich',
    color: 'text-blue-400',
  },
  {
    icon: <WebIcon sx={{ fontSize: 40 }} />,
    title: 'Web Applications',
    description: 'Full-stack web apps with FastAPI and Next.js',
    color: 'text-green-400',
  },
  {
    icon: <DesktopIcon sx={{ fontSize: 40 }} />,
    title: 'Desktop GUI',
    description: 'Cross-platform desktop applications with NiceGUI',
    color: 'text-purple-400',
  },
  {
    icon: <SecurityIcon sx={{ fontSize: 40 }} />,
    title: 'Authentication',
    description: 'Secure JWT-based authentication and authorization',
    color: 'text-red-400',
  },
  {
    icon: <SpeedIcon sx={{ fontSize: 40 }} />,
    title: 'High Performance',
    description: 'Async/await patterns with SQLModel and AsyncPG',
    color: 'text-yellow-400',
  },
  {
    icon: <CloudIcon sx={{ fontSize: 40 }} />,
    title: 'Real-time Features',
    description: 'WebSocket support for live updates and notifications',
    color: 'text-cyan-400',
  },
  {
    icon: <AnalyticsIcon sx={{ fontSize: 40 }} />,
    title: 'Monitoring',
    description: 'Comprehensive observability with structured logging',
    color: 'text-orange-400',
  },
  {
    icon: <DashboardIcon sx={{ fontSize: 40 }} />,
    title: 'Modern UI',
    description: 'Beautiful dark-themed interface with Material-UI',
    color: 'text-pink-400',
  },
];

export default function HomePage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Container maxWidth="lg" className="py-8">
        <Box className="flex justify-center items-center min-h-96">
          <Typography variant="h6" className="text-gray-400">
            Loading...
          </Typography>
        </Box>
      </Container>
    );
  }

  if (user) {
    // Authenticated user sees the dashboard
    return (
      <Container maxWidth="lg" className="py-8">
        <Box className="mb-8">
          <Typography variant="h3" className="text-gradient font-bold mb-2">
            Welcome back, {user.full_name || user.username}!
          </Typography>
          <Typography variant="body1" className="text-gray-400">
            Here's what's happening with your Full-Stack Python Kit
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {/* Dashboard Stats */}
          <Grid item xs={12}>
            <DashboardStats />
          </Grid>

          {/* Quick Actions */}
          <Grid item xs={12} md={4}>
            <QuickActions />
          </Grid>

          {/* Recent Activity */}
          <Grid item xs={12} md={8}>
            <RecentActivity />
          </Grid>
        </Grid>
      </Container>
    );
  }

  // Unauthenticated users see the landing page
  return (
    <Container maxWidth="lg" className="py-8">
      {/* Hero Section */}
      <Box className="text-center mb-12">
        <Typography variant="h1" className="text-gradient font-bold mb-4">
          Full-Stack Python Kit
        </Typography>
        <Typography variant="h5" className="text-gray-300 mb-6 max-w-2xl mx-auto">
          A comprehensive monorepo for building CLI, GUI, and web applications with modern Python
        </Typography>
        <Box className="flex gap-4 justify-center">
          <Button
            component={Link}
            href="/auth/login"
            variant="contained"
            size="large"
            className="btn-primary px-8 py-3"
          >
            Get Started
          </Button>
          <Button
            component={Link}
            href="/auth/register"
            variant="outlined"
            size="large"
            className="px-8 py-3 border-primary-500 text-primary-400 hover:bg-primary-500 hover:text-white"
          >
            Sign Up
          </Button>
        </Box>
      </Box>

      {/* Features Grid */}
      <Box className="mb-12">
        <Typography variant="h3" className="text-center mb-8 text-white">
          Everything You Need
        </Typography>
        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card className="h-full hover:shadow-xl transition-shadow duration-300">
                <CardContent className="text-center p-6">
                  <Box className={`mb-4 ${feature.color}`}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" className="mb-2 text-white font-semibold">
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" className="text-gray-400">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Tech Stack Section */}
      <Box className="text-center">
        <Typography variant="h3" className="mb-6 text-white">
          Modern Tech Stack
        </Typography>
        <Typography variant="body1" className="text-gray-400 mb-8 max-w-3xl mx-auto">
          Built with the latest and greatest Python technologies including FastAPI, SQLModel, 
          Next.js, TypeScript, Tailwind CSS, and more. Everything you need for rapid development 
          and production deployment.
        </Typography>
        
        <Grid container spacing={2} className="max-w-4xl mx-auto">
          {[
            'FastAPI', 'Next.js', 'TypeScript', 'SQLModel', 'PostgreSQL', 'Redis',
            'Typer', 'NiceGUI', 'Material-UI', 'Tailwind CSS', 'Zustand', 'WebSockets'
          ].map((tech) => (
            <Grid item xs={6} sm={4} md={3} key={tech}>
              <Box className="bg-dark-800 rounded-lg p-3 border border-dark-700">
                <Typography variant="body2" className="text-primary-400 font-medium">
                  {tech}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}