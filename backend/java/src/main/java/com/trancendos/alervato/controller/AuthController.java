package com.trancendos.alervato.controller;

import com.trancendos.alervato.dto.LoginRequest;
import com.trancendos.alervato.dto.LoginResponse;
import com.trancendos.alervato.dto.RegisterRequest;
import com.trancendos.alervato.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Controller for handling user authentication operations.
 * <p>
 * This class provides REST endpoints for user registration, login, and logout.
 * It delegates the business logic to the {@link AuthService}.
 *
 * @author Trancendos
 * @version 1.0
 */
@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private AuthService authService;

    /**
     * Registers a new user in the system.
     *
     * @param registerRequest The request body containing the user's registration details.
     * @return A {@link ResponseEntity} indicating the result of the registration attempt.
     */
    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@Valid @RequestBody RegisterRequest registerRequest) {
        try {
            authService.registerUser(registerRequest);
            return ResponseEntity.ok().body("User registered successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Authenticates an existing user and returns a JWT token.
     *
     * @param loginRequest The request body containing the user's login credentials.
     * @return A {@link ResponseEntity} containing the {@link LoginResponse} with the JWT token.
     */
    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {
        try {
            LoginResponse response = authService.authenticateUser(loginRequest);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Logs out the currently authenticated user.
     *
     * @param token The JWT token of the user to be logged out.
     * @return A {@link ResponseEntity} indicating the result of the logout attempt.
     */
    @PostMapping("/logout")
    public ResponseEntity<?> logoutUser(@RequestHeader("Authorization") String token) {
        try {
            authService.logoutUser(token);
            return ResponseEntity.ok().body("User logged out successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}