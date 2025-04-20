import { Box, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import InventoryIcon from '@mui/icons-material/Inventory';
import FactoryIcon from '@mui/icons-material/Factory';
import LanguageIcon from '@mui/icons-material/Language';

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Orders', icon: <ShoppingCartIcon />, path: '/orders' },
  { text: 'Inventory', icon: <InventoryIcon />, path: '/inventory' },
  { text: 'Manufacturing', icon: <FactoryIcon />, path: '/manufacturing' },
  { text: 'Website', icon: <LanguageIcon />, path: '/website' },
];

export default function Sidebar() {
  return (
    <Box
      sx={{
        width: 240,
        bgcolor: 'background.paper',
        borderRight: 1,
        borderColor: 'divider',
      }}
    >
      <List>
        {menuItems.map((item) => (
          <ListItem
            key={item.text}
            button
            sx={{
              '&:hover': {
                bgcolor: 'action.hover',
              },
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}