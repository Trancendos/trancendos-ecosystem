package com.trancendos.alervato.controller;

import com.trancendos.alervato.dto.TransactionDTO;
import com.trancendos.alervato.model.Transaction;
import com.trancendos.alervato.service.TransactionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for handling financial transaction operations.
 * <p>
 * This class provides REST endpoints for creating, retrieving, updating, and deleting
 * transactions for the authenticated user. It uses {@link TransactionService} to
 * perform the business logic.
 *
 * @author Trancendos
 * @version 1.0
 */
@RestController
@RequestMapping("/api/transactions")
@CrossOrigin(origins = "*")
public class TransactionController {

    @Autowired
    private TransactionService transactionService;

    /**
     * Retrieves a paginated list of transactions for the authenticated user.
     *
     * @param authentication The authentication object containing the user's details.
     * @param pageable       The pagination information.
     * @return A {@link ResponseEntity} containing a {@link Page} of {@link Transaction} objects.
     */
    @GetMapping
    public ResponseEntity<Page<Transaction>> getUserTransactions(
            Authentication authentication,
            Pageable pageable) {
        String username = authentication.getName();
        Page<Transaction> transactions = transactionService.getUserTransactions(username, pageable);
        return ResponseEntity.ok(transactions);
    }

    /**
     * Creates a new transaction for the authenticated user.
     *
     * @param transactionDTO The request body containing the new transaction's details.
     * @param authentication The authentication object containing the user's details.
     * @return A {@link ResponseEntity} containing the created {@link Transaction}.
     */
    @PostMapping
    public ResponseEntity<?> createTransaction(
            @Valid @RequestBody TransactionDTO transactionDTO,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.createTransaction(transactionDTO, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Retrieves a specific transaction by its ID.
     *
     * @param id             The ID of the transaction to retrieve.
     * @param authentication The authentication object containing the user's details.
     * @return A {@link ResponseEntity} containing the requested {@link Transaction}.
     */
    @GetMapping("/{id}")
    public ResponseEntity<?> getTransaction(
            @PathVariable Long id,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.getTransactionById(id, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * Updates an existing transaction.
     *
     * @param id             The ID of the transaction to update.
     * @param transactionDTO The request body containing the updated transaction details.
     * @param authentication The authentication object containing the user's details.
     * @return A {@link ResponseEntity} containing the updated {@link Transaction}.
     */
    @PutMapping("/{id}")
    public ResponseEntity<?> updateTransaction(
            @PathVariable Long id,
            @Valid @RequestBody TransactionDTO transactionDTO,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.updateTransaction(id, transactionDTO, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Deletes a transaction by its ID.
     *
     * @param id             The ID of the transaction to delete.
     * @param authentication The authentication object containing the user's details.
     * @return A {@link ResponseEntity} indicating the result of the deletion attempt.
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTransaction(
            @PathVariable Long id,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            transactionService.deleteTransaction(id, username);
            return ResponseEntity.ok().body("Transaction deleted successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}