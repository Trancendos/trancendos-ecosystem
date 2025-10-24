package com.trancendos.alervato.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Represents a single financial transaction in the system.
 * <p>
 * This entity is mapped to the "transactions" table in the database and contains
 * details about the transaction, such as its amount, type, and associated user.
 *
 * @author Trancendos
 * @version 1.0
 */
@Entity
@Table(name = "transactions")
@EntityListeners(AuditingEntityListener.class)
public class Transaction {
    
    /**
     * The unique identifier for the transaction.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * The monetary value of the transaction.
     */
    @NotNull
    @DecimalMin(value = "0.0", inclusive = false)
    @Column(nullable = false, precision = 19, scale = 2)
    private BigDecimal amount;
    
    /**
     * A brief description of the transaction.
     */
    @Column(length = 500)
    private String description;
    
    /**
     * The type of the transaction (e.g., INCOME, EXPENSE).
     */
    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TransactionType type;
    
    /**
     * The category of the transaction (e.g., "Groceries", "Salary").
     */
    @Column(length = 100)
    private String category;
    
    /**
     * The user who made the transaction.
     */
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    /**
     * The timestamp when the transaction was created.
     */
    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * The timestamp when the transaction was last updated.
     */
    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    /**
     * The actual date of the transaction.
     */
    @Column(name = "transaction_date")
    private LocalDateTime transactionDate;
    
    /**
     * A unique reference number for the transaction.
     */
    @Column(name = "reference_number", unique = true)
    private String referenceNumber;
    
    /**
     * Enumeration for the type of a financial transaction.
     */
    public enum TransactionType {
        INCOME, EXPENSE, TRANSFER
    }
    
    /**
     * Default constructor.
     */
    public Transaction() {}
    
    /**
     * Constructs a new Transaction with the specified details.
     *
     * @param amount      The amount of the transaction.
     * @param description A description of the transaction.
     * @param type        The type of the transaction.
     * @param user        The user associated with the transaction.
     */
    public Transaction(BigDecimal amount, String description, TransactionType type, User user) {
        this.amount = amount;
        this.description = description;
        this.type = type;
        this.user = user;
        this.transactionDate = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public TransactionType getType() { return type; }
    public void setType(TransactionType type) { this.type = type; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public LocalDateTime getTransactionDate() { return transactionDate; }
    public void setTransactionDate(LocalDateTime transactionDate) { this.transactionDate = transactionDate; }
    
    public String getReferenceNumber() { return referenceNumber; }
    public void setReferenceNumber(String referenceNumber) { this.referenceNumber = referenceNumber; }
}