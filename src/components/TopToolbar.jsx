import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Tooltip
} from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import BoltIcon from '@mui/icons-material/FlashOn';
import GitHubIcon from '@mui/icons-material/GitHub';

const TopToolbar = () => (
  <AppBar position="fixed" color="transparent" elevation={1} sx={{ zIndex: 1201 }}>
    <Toolbar sx={{ justifyContent: 'space-between' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Typography sx={{ fontWeight: 600, fontSize: 16 }}>❤️ -inventory-flow</Typography>
        <Button
          size="small"
          variant="outlined"
          sx={{
            textTransform: 'none',
            color: 'white',
            borderColor: 'gray'
          }}
        >
          Home ▾
        </Button>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Tooltip title="View code"><IconButton><CodeIcon /></IconButton></Tooltip>
        <Tooltip title="Bolt"><IconButton><BoltIcon /></IconButton></Tooltip>
        <Tooltip title="GitHub"><IconButton><GitHubIcon /></IconButton></Tooltip>
        <Button variant="contained">Publish</Button>
      </Box>
    </Toolbar>
  </AppBar>
);

export default TopToolbar;
