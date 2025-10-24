package com.trancendos.alervato.service;

import com.trancendos.alervato.dto.LoginRequest;
import com.trancendos.alervato.dto.LoginResponse;
import com.trancendos.alervato.dto.RegisterRequest;
import com.trancendos.alervato.model.Role;
import com.trancendos.alervato.model.User;
import com.trancendos.alervato.repository.RoleRepository;
import com.trancendos.alervato.repository.UserRepository;
import com.trancendos.alervato.security.JwtUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.Set;

@Service
public class AuthService {
    
    @Autowired
    private AuthenticationManager authenticationManager;
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private RoleRepository roleRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private JwtUtils jwtUtils;
    
    public void registerUser(RegisterRequest registerRequest) {
        if (userRepository.existsByUsername(registerRequest.getUsername())) {
            throw new RuntimeException("Username is already taken!");
        }
        
        if (userRepository.existsByEmail(registerRequest.getEmail())) {
            throw new RuntimeException("Email is already in use!");
        }
        
        // Create new user account
        User user = new User(registerRequest.getUsername(),
                           registerRequest.getEmail(),
                           passwordEncoder.encode(registerRequest.getPassword()));
        
        user.setFirstName(registerRequest.getFirstName());
        user.setLastName(registerRequest.getLastName());
        
        Set<Role> roles = new HashSet<>();
        Role userRole = roleRepository.findByName("ROLE_USER")
                .orElseThrow(() -> new RuntimeException("Role not found"));
        roles.add(userRole);
        
        user.setRoles(roles);
        userRepository.save(user);
    }
    
    public LoginResponse authenticateUser(LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword()));
        
        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = jwtUtils.generateJwtToken(authentication);
        
        User user = userRepository.findByUsername(loginRequest.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        return new LoginResponse(jwt, user.getId(), user.getUsername(), user.getEmail());
    }
    
    public void logoutUser(String token) {
        // Add token to blacklist (implement as needed)
        SecurityContextHolder.clearContext();
    }
}