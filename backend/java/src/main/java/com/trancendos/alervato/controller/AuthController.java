package com.trancendos.alervato.controller;

import com.trancendos.alervato.dto.LoginRequest;
import com.trancendos.alervato.dto.LoginResponse;
import com.trancendos.alervato.dto.RegisterRequest;
import com.trancendos.alervato.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private AuthService authService;

    /**
     * Registers a new user.
     *
     * @param registerRequest The request body containing the user's registration details.
     * @return A `ResponseEntity` indicating the result of the registration attempt.
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
     * Authenticates a user.
     *
     * @param loginRequest The request body containing the user's login credentials.
     * @return A `ResponseEntity` containing the login response, or an error message.
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
     * Logs out a user.
     *
     * @param token The authorization token of the user to be logged out.
     * @return A `ResponseEntity` indicating the result of the logout attempt.
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