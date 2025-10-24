package com.trancendos.alervato.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

/**
 * Represents a user of the application.
 * <p>
 * This entity is mapped to the "users" table in the database and contains
 * personal and authentication information for a user.
 *
 * @author Trancendos
 * @version 1.0
 */
@Entity
@Table(name = "users", uniqueConstraints = {
        @UniqueConstraint(columnNames = "username"),
        @UniqueConstraint(columnNames = "email")
})
@EntityListeners(AuditingEntityListener.class)
public class User {
    
    /**
     * The unique identifier for the user.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * The user's unique username.
     */
    @NotBlank
    @Column(nullable = false, unique = true)
    private String username;
    
    /**
     * The user's unique email address.
     */
    @NotBlank
    @Email
    @Column(nullable = false, unique = true)
    private String email;
    
    /**
     * The user's hashed password.
     */
    @NotBlank
    @Column(nullable = false)
    private String password;
    
    /**
     * The user's first name.
     */
    @Column(name = "first_name")
    private String firstName;
    
    /**
     * The user's last name.
     */
    @Column(name = "last_name")
    private String lastName;
    
    /**
     * The user's phone number.
     */
    @Column(name = "phone_number")
    private String phoneNumber;
    
    /**
     * A flag indicating whether the user's account is active.
     */
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    /**
     * The timestamp when the user account was created.
     */
    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * The timestamp when the user account was last updated.
     */
    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    /**
     * The set of roles assigned to the user.
     */
    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "user_roles",
            joinColumns = @JoinColumn(name = "user_id"),
            inverseJoinColumns = @JoinColumn(name = "role_id"))
    private Set<Role> roles = new HashSet<>();
    
    /**
     * Default constructor.
     */
    public User() {}
    
    /**
     * Constructs a new User with the specified username, email, and password.
     *
     * @param username The user's username.
     * @param email    The user's email address.
     * @param password The user's password.
     */
    public User(String username, String email, String password) {
        this.username = username;
        this.email = email;
        this.password = password;
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    
    public String getPhoneNumber() { return phoneNumber; }
    public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }
    
    public Boolean getIsActive() { return isActive; }
    public void setIsActive(Boolean isActive) { this.isActive = isActive; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public Set<Role> getRoles() { return roles; }
    public void setRoles(Set<Role> roles) { this.roles = roles; }
}